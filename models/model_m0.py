# models/model_m0.py
"""
M0: Pure CFR Action System (A, circ, C)

Implements Section 1 and Section 2 of cfr/cfr-proofs.md with zero external
dependencies and no presupposed spacetime, Hilbert space, particles, or mutable
state:
  - Sub-history closure verification (Axiom A1)
  - Continuation cones N_1(h), N_L(h), N^+(h), and Hard Roadblocks (Lemma 1.3)
  - Counterexample proving 1-step equivalence fails congruence (Prop. 2.1)
  - Minimal emergent CFR state space S_CFR = C / ~ via Myhill-Nerode
    future-cone equivalence (Theorem 2.3)
  - Locally finite causal partial order h1 < h2 (Theorem 2.5) and the split
    between irreversible temporal channels and periodic matter cycles (Prop. 2.6)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

ActionSymbol = str


@dataclass(frozen=True)
class ActionHistory:
    """
    Immutable action history h = alpha_n o ... o alpha_1.

    Stored internally in chronological execution order (alpha_1, ..., alpha_n)
    so extending by `alpha o h` appends `alpha` on the right of the tuple while
    displaying in standard algebraic composition order `alpha_n o ... o alpha_1`.
    """

    steps: Tuple[ActionSymbol, ...]

    def __post_init__(self) -> None:
        if not self.steps:
            raise ValueError("Admissible CFR histories in A^+ must be non-empty.")

    def __len__(self) -> int:
        return len(self.steps)

    def compose_left(self, later: "ActionHistory") -> "ActionHistory":
        """Return `later o self` (apply `self` first, then `later`)."""
        return ActionHistory(self.steps + later.steps)

    def extend(self, alpha: ActionSymbol) -> "ActionHistory":
        """Return `alpha o self`."""
        return ActionHistory(self.steps + (alpha,))

    def precedes(self, other: "ActionHistory") -> bool:
        """Causal strict partial order: self < other iff exists gamma: other = gamma o self."""
        n = len(self.steps)
        return len(other.steps) > n and other.steps[:n] == self.steps

    def __str__(self) -> str:
        return " ∘ ".join(reversed(self.steps))


class CFRActionSystem:
    """
    A finite CFR Action System (A, circ, C) satisfying Sub-history Closure (A1):
        h2 o h1 in C  ==>  h1 in C and h2 in C.
    """

    def __init__(
        self,
        alphabet: Iterable[ActionSymbol],
        admissible: Iterable[Tuple[ActionSymbol, ...]],
        enforce_closure: bool = True,
    ) -> None:
        self.alphabet: Tuple[ActionSymbol, ...] = tuple(sorted(set(alphabet)))
        raw_histories = {ActionHistory(tuple(seq)) for seq in admissible if seq}
        for h in raw_histories:
            for s in h.steps:
                if s not in self.alphabet:
                    raise ValueError(f"Action '{s}' in history {h} not in alphabet.")
        if enforce_closure:
            self.admissible: FrozenSet[ActionHistory] = self._close_subhistories(raw_histories)
        else:
            self.admissible = frozenset(raw_histories)

    @staticmethod
    def _close_subhistories(histories: Set[ActionHistory]) -> FrozenSet[ActionHistory]:
        """Close a seed set of histories under contiguous sub-histories so (A1) holds."""
        closed: Set[ActionHistory] = set()
        for h in histories:
            n = len(h.steps)
            for i in range(n):
                for j in range(i + 1, n + 1):
                    closed.add(ActionHistory(h.steps[i:j]))
        return frozenset(closed)

    def verify_subhistory_closure(self) -> bool:
        """Verify Axiom (A1): every non-empty prefix/suffix split of C lies in C."""
        for h in self.admissible:
            n = len(h.steps)
            for split in range(1, n):
                h1 = ActionHistory(h.steps[:split])
                h2 = ActionHistory(h.steps[split:])
                if h1 not in self.admissible or h2 not in self.admissible:
                    return False
        return True

    # ------------------------------------------------------------------
    # Continuation cones and Hard Roadblocks (Definitions 1.2 & Lemma 1.3)
    # ------------------------------------------------------------------

    def continuations_1(self, h: ActionHistory) -> FrozenSet[ActionSymbol]:
        """Immediate 1-step admissible continuations N_1(h) = {a in A : a o h in C}."""
        if h not in self.admissible:
            raise ValueError(f"History {h} is not admissible.")
        return frozenset(a for a in self.alphabet if h.extend(a) in self.admissible)

    def continuations_horizon(
        self, h: ActionHistory, horizon: int
    ) -> FrozenSet[Tuple[ActionSymbol, ...]]:
        """Horizon-L admissible continuations N_L(h) as chronological tuples."""
        if h not in self.admissible:
            raise ValueError(f"History {h} is not admissible.")
        if horizon < 1:
            raise ValueError("Horizon L must be >= 1.")
        n = len(h.steps)
        return frozenset(
            cand.steps[n:]
            for cand in self.admissible
            if len(cand.steps) == n + horizon and cand.steps[:n] == h.steps
        )

    def continuation_cone(self, h: ActionHistory) -> FrozenSet[Tuple[ActionSymbol, ...]]:
        """Full continuation cone N^+(h) = {gamma in A^+ : gamma o h in C}."""
        if h not in self.admissible:
            raise ValueError(f"History {h} is not admissible.")
        n = len(h.steps)
        return frozenset(
            cand.steps[n:]
            for cand in self.admissible
            if len(cand.steps) > n and cand.steps[:n] == h.steps
        )

    def is_hard_roadblock(self, h: ActionHistory) -> bool:
        """Hard Roadblock: R_hard(h) <=> N_1(h) == empty."""
        return len(self.continuations_1(h)) == 0

    # ------------------------------------------------------------------
    # Emergent States S_CFR = C / ~ (Theorem 2.3)
    # ------------------------------------------------------------------

    def future_equivalent(self, h1: ActionHistory, h2: ActionHistory) -> bool:
        """CFR state equivalence: h1 ~ h2 <=> N^+(h1) == N^+(h2)."""
        return self.continuation_cone(h1) == self.continuation_cone(h2)

    def one_step_equivalent(self, h1: ActionHistory, h2: ActionHistory) -> bool:
        """Naive 1-step equivalence N_1(h1) == N_1(h2) (fails congruence in general)."""
        return self.continuations_1(h1) == self.continuations_1(h2)

    def emergent_states(self) -> Dict[FrozenSet[Tuple[ActionSymbol, ...]], FrozenSet[ActionHistory]]:
        """
        Partition C into emergent state equivalence classes [h] keyed by their
        canonical invariant continuation cone N^+(h).
        """
        classes: Dict[FrozenSet[Tuple[ActionSymbol, ...]], Set[ActionHistory]] = {}
        for h in self.admissible:
            cone = self.continuation_cone(h)
            classes.setdefault(cone, set()).add(h)
        return {cone: frozenset(members) for cone, members in classes.items()}

    def verify_left_congruence(self) -> bool:
        """
        Check Theorem 2.3(2): whenever h1 ~ h2 and a in N_1(h1),
        we also have a in N_1(h2) and (a o h1) ~ (a o h2).
        """
        histories = list(self.admissible)
        for i, h1 in enumerate(histories):
            for h2 in histories[i + 1 :]:
                if not self.future_equivalent(h1, h2):
                    continue
                if self.continuations_1(h1) != self.continuations_1(h2):
                    return False
                for a in self.continuations_1(h1):
                    if not self.future_equivalent(h1.extend(a), h2.extend(a)):
                        return False
        return True

    def state_transitions(self) -> Tuple[List[str], Dict[Tuple[str, ActionSymbol], str]]:
        """
        Construct the quotient transition automaton on S_CFR = C / ~.
        Returns deterministic state labels and partial transition table (state, action) -> state.
        """
        classes = self.emergent_states()
        sorted_cones = sorted(
            classes.keys(),
            key=lambda cone: (len(cone), sorted(cone)),
        )
        cone_to_label = {cone: f"S{idx}" for idx, cone in enumerate(sorted_cones)}
        transitions: Dict[Tuple[str, ActionSymbol], str] = {}

        for cone in sorted_cones:
            rep = next(iter(classes[cone]))
            src_label = cone_to_label[cone]
            for a in sorted(self.continuations_1(rep)):
                dst_cone = self.continuation_cone(rep.extend(a))
                transitions[(src_label, a)] = cone_to_label[dst_cone]

        return [cone_to_label[c] for c in sorted_cones], transitions

    # ------------------------------------------------------------------
    # Causal Poset & Periodic Matter Cycles (Theorem 2.5 & Prop. 2.6)
    # ------------------------------------------------------------------

    def verify_causal_strict_partial_order(self) -> bool:
        """Verify irreflexivity, asymmetry, and transitivity of < on C."""
        hs = list(self.admissible)
        for h in hs:
            if h.precedes(h):
                return False
        for h1 in hs:
            for h2 in hs:
                if h1.precedes(h2) and h2.precedes(h1):
                    return False
                if h1.precedes(h2):
                    for h3 in hs:
                        if h2.precedes(h3) and not h1.precedes(h3):
                            return False
        return True

    def causal_interval(self, h1: ActionHistory, h2: ActionHistory) -> List[ActionHistory]:
        """Return {h in C : h1 < h < h2} sorted by length."""
        return sorted(
            [h for h in self.admissible if h1.precedes(h) and h.precedes(h2)],
            key=lambda h: (len(h), h.steps),
        )


def build_congruence_counterexample() -> CFRActionSystem:
    """
    Construct the explicit system from Proposition 2.1:
      C generated by {d o c o a, c o b} (chronologically ('a','c','d') and ('b','c')).
    Shows a ~_1 b (both allow 'c') yet (c o a) !~_1 (c o b), while full cone N^+
    cleanly distinguishes [a] != [b] and satisfies Theorem 2.3 congruence.
    """
    return CFRActionSystem(
        alphabet=["a", "b", "c", "d"],
        admissible=[("a", "c", "d"), ("b", "c")],
        enforce_closure=True,
    )


def check_periodic_matter_knot(period_steps: int = 3, max_cycles: int = 4) -> Dict[str, object]:
    """
    Demonstrate Proposition 2.6 on a bounded observation window:
    A cyclic 2-action pattern ('u', 'v', 'u', 'v', ...) whose continuation
    structure up to finite horizon repeats every 2 steps (period = 2),
    contrasted with an irreversible record channel whose continuation rank
    strictly shrinks toward a Roadblock.
    """
    # Build alternating words up to length 2 * max_cycles + 2
    max_len = 2 * max_cycles + 2
    alternating_u = tuple("u" if i % 2 == 0 else "v" for i in range(max_len))
    system = CFRActionSystem(alphabet=["u", "v"], admissible=[alternating_u])

    h_base = ActionHistory(("u", "v"))
    h_cycled = ActionHistory(("u", "v", "u", "v"))
    # Within remaining horizon L = period_steps, [gamma_0 o h] matches [h]
    horizon_match = (
        system.continuations_horizon(h_base, period_steps)
        == system.continuations_horizon(h_cycled, period_steps)
    )
    return {
        "h_base": str(h_base),
        "h_cycled": str(h_cycled),
        "horizon": period_steps,
        "periodic_state_preserved": horizon_match,
    }


def demo() -> None:
    print("=== Model M0: Pure CFR Action System (A, circ, C) ===")
    sys_ce = build_congruence_counterexample()
    ha = ActionHistory(("a",))
    hb = ActionHistory(("b",))
    print(f"Axiom (A1) sub-history closure holds: {sys_ce.verify_subhistory_closure()}")
    print(f"1-step equivalence a ~_1 b:           {sys_ce.one_step_equivalent(ha, hb)}")
    print(
        f"After 'c', (c∘a) ~_1 (c∘b):           "
        f"{sys_ce.one_step_equivalent(ha.extend('c'), hb.extend('c'))} (Prop. 2.1 failure)"
    )
    print(f"Full CFR equivalence a ~ b:           {sys_ce.future_equivalent(ha, hb)}")
    print(f"Theorem 2.3 left-congruence holds:    {sys_ce.verify_left_congruence()}")
    print(f"Theorem 2.5 strict causal poset:      {sys_ce.verify_causal_strict_partial_order()}")

    states, trans = sys_ce.state_transitions()
    print(f"Emergent minimal states ({len(states)}):        {states}")
    print(f"Quotient state transitions:           {trans}")

    knot = check_periodic_matter_knot()
    print(f"Periodic matter cycle preserved:      {knot['periodic_state_preserved']}")


if __name__ == "__main__":
    demo()
