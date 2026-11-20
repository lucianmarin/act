# models/model_m1.py
"""
M1: CFR Quantum Action Network (A, circ, C, Z, G)

Restores and extends the original zero-dependency FiniteActionModel for CFR:
  - Multiplicative complex amplitudes Z(beta o alpha) = Z(beta) Z(alpha)
  - Coherent path summation K(X_f, X_i) = sum_gamma Z(gamma) and interference
  - Constraint interventions and causal influence detection
  - Local U(1) gauge rephasing invariance
  - Non-factorizable composite entanglement (rank C_ij > 1) with no-signalling
  - Numerical verification of Theorem 4.2: Born's rule P(z) = |z|^2 is the
    unique power law P(z) = |z|^alpha conserving probability across two-stage
    symmetric CFR interference networks.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, replace
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple

Node = str
Path = Tuple[str, ...]


def matrix_rank(mat: List[List[complex]], tol: float = 1e-10) -> int:
    """Compute the rank of a complex matrix using Gaussian elimination."""
    if not mat or not mat[0]:
        return 0

    n_rows = len(mat)
    n_cols = len(mat[0])
    m = [row[:] for row in mat]
    rank = 0

    for col in range(n_cols):
        pivot = None
        best_mag = tol
        for r in range(rank, n_rows):
            mag = abs(m[r][col])
            if mag > best_mag:
                best_mag = mag
                pivot = r
        if pivot is None:
            continue

        m[rank], m[pivot] = m[pivot], m[rank]
        pivot_val = m[rank][col]
        for c in range(col, n_cols):
            m[rank][c] /= pivot_val

        for r in range(n_rows):
            if r == rank:
                continue
            factor = m[r][col]
            if abs(factor) <= tol:
                continue
            for c in range(col, n_cols):
                m[r][c] -= factor * m[rank][c]

        rank += 1
        if rank == n_rows:
            break

    return rank


@dataclass(frozen=True)
class Action:
    """
    An elementary action transition between emergent CFR states / boundary labels.
    Nodes are emergent state labels [h] in S_CFR, not presupposed spacetime points.
    """

    name: str
    src: Node
    dst: Node
    weight: complex = 1.0 + 0.0j


class FiniteActionModel:
    """
    Finite CFR action category/graph (A, circ, C, Z, G).
    """

    def __init__(
        self,
        actions: Iterable[Action],
        disabled: Optional[Set[str]] = None,
        path_constraint: Optional[Callable[[Path], bool]] = None,
    ) -> None:
        self.actions: Dict[str, Action] = {a.name: a for a in actions}
        self.disabled: Set[str] = set(disabled) if disabled is not None else set()
        self.path_constraint = path_constraint

    def nodes(self) -> List[Node]:
        node_set: Set[Node] = set()
        for a in self.actions.values():
            node_set.add(a.src)
            node_set.add(a.dst)
        return sorted(node_set)

    def outgoing(self, node: Node) -> List[Action]:
        return sorted(
            [
                a
                for a in self.actions.values()
                if a.src == node and a.name not in self.disabled
            ],
            key=lambda x: x.name,
        )

    def is_action_allowed(self, name: str) -> bool:
        return name in self.actions and name not in self.disabled

    def path_allowed(self, path: Path) -> bool:
        for name in path:
            if not self.is_action_allowed(name):
                return False
        if self.path_constraint is not None and not self.path_constraint(path):
            return False
        return True

    def with_disabled(self, extra_disabled: Iterable[str]) -> "FiniteActionModel":
        return FiniteActionModel(
            actions=self.actions.values(),
            disabled=self.disabled.union(set(extra_disabled)),
            path_constraint=self.path_constraint,
        )

    def path_weight(self, path: Path) -> complex:
        w = 1.0 + 0.0j
        for name in path:
            if not self.is_action_allowed(name):
                return 0.0 + 0.0j
            w *= self.actions[name].weight
        return w

    def endpoint_after_path(self, start: Node, path: Path) -> Optional[Node]:
        node = start
        for name in path:
            if not self.is_action_allowed(name):
                return None
            action = self.actions[name]
            if action.src != node:
                return None
            node = action.dst
        return node

    def iter_paths(
        self,
        start: Node,
        end: Optional[Node] = None,
        max_depth: int = 4,
        min_depth: int = 0,
        exact_depth: Optional[int] = None,
    ) -> Iterable[Path]:
        if exact_depth is not None:
            min_depth = exact_depth
            max_depth = exact_depth

        stack: List[Tuple[Node, Path]] = [(start, tuple())]
        while stack:
            node, path = stack.pop()
            if len(path) >= min_depth and (end is None or node == end):
                yield path
            if len(path) >= max_depth:
                continue
            for action in reversed(self.outgoing(node)):
                new_path = path + (action.name,)
                if self.path_allowed(new_path):
                    stack.append((action.dst, new_path))

    def transition_amplitude(
        self,
        src: Node,
        dst: Node,
        max_depth: int = 4,
        min_depth: int = 0,
        exact_depth: Optional[int] = None,
    ) -> complex:
        total = 0.0 + 0.0j
        for path in self.iter_paths(
            start=src,
            end=dst,
            max_depth=max_depth,
            min_depth=min_depth,
            exact_depth=exact_depth,
        ):
            total += self.path_weight(path)
        return total

    def transition_probability(
        self,
        src: Node,
        dst: Node,
        max_depth: int = 4,
        min_depth: int = 0,
        exact_depth: Optional[int] = None,
    ) -> float:
        amp = self.transition_amplitude(
            src,
            dst,
            max_depth=max_depth,
            min_depth=min_depth,
            exact_depth=exact_depth,
        )
        return abs(amp) ** 2

    def continuations(self, node: Node, max_depth: int = 3) -> List[Path]:
        return list(self.iter_paths(start=node, end=None, max_depth=max_depth, min_depth=1))


def gauge_transform(
    model: FiniteActionModel,
    phases: Dict[Node, float],
) -> FiniteActionModel:
    """
    Local U(1) action rephasing: Z'(u -> v) = exp(i theta_u) Z(u -> v) exp(-i theta_v).
    """
    new_actions: List[Action] = []
    for a in model.actions.values():
        theta_src = phases.get(a.src, 0.0)
        theta_dst = phases.get(a.dst, 0.0)
        new_weight = a.weight * cmath.exp(1j * (theta_src - theta_dst))
        new_actions.append(replace(a, weight=new_weight))
    return FiniteActionModel(
        actions=new_actions,
        disabled=model.disabled,
        path_constraint=model.path_constraint,
    )


def intervention_effect(
    model: FiniteActionModel,
    src: Node,
    dst: Node,
    intervention_disabled: Iterable[str],
    max_depth: int = 4,
    tol: float = 1e-12,
) -> Dict[str, object]:
    """Check whether disabling actions alters P(src -> dst)."""
    p_before = model.transition_probability(src, dst, max_depth=max_depth)
    intervened = model.with_disabled(intervention_disabled)
    p_after = intervened.transition_probability(src, dst, max_depth=max_depth)
    delta = p_after - p_before
    return {
        "p_before": p_before,
        "p_after": p_after,
        "delta": delta,
        "effect": abs(delta) > tol,
    }


def verify_born_rule_exponent(alpha: float) -> Dict[str, float]:
    """
    Numerically test Theorem 4.2 for any candidate probability rule P(z) = |z|^alpha.

    Constructs the two-stage symmetric CFR action network:
      Stage 1: s0 -> m1 (r), s0 -> m2 (r)
      Stage 2: m1 -> f1 (r), m1 -> f2 (r), m2 -> f1 (r), m2 -> f2 (-r)
    where single-stage conservation 2 * r^alpha = 1 fixes r = 2^(-1/alpha).
    Returns total two-stage exit probability P(K(s0->f1)) + P(K(s0->f2)) = 2^(alpha - 2),
    which equals 1.0 if and only if alpha == 2.0.
    """
    if alpha <= 0:
        raise ValueError("Exponent alpha must be positive.")
    r = 2.0 ** (-1.0 / alpha)
    model = FiniteActionModel(
        [
            Action("s0->m1", "s0", "m1", r + 0.0j),
            Action("s0->m2", "s0", "m2", r + 0.0j),
            Action("m1->f1", "m1", "f1", r + 0.0j),
            Action("m1->f2", "m1", "f2", r + 0.0j),
            Action("m2->f1", "m2", "f1", r + 0.0j),
            Action("m2->f2", "m2", "f2", -r + 0.0j),
        ]
    )
    k_f1 = model.transition_amplitude("s0", "f1", exact_depth=2)
    k_f2 = model.transition_amplitude("s0", "f2", exact_depth=2)
    p_total = (abs(k_f1) ** alpha) + (abs(k_f2) ** alpha)
    return {
        "alpha": alpha,
        "r": r,
        "amp_f1": abs(k_f1),
        "amp_f2": abs(k_f2),
        "two_stage_total_prob": p_total,
        "conservation_error": p_total - 1.0,
    }


def build_bipartite_action_experiment(entangled: bool = True, phi_a: float = 0.0) -> Dict[str, object]:
    """
    Build a bipartite CFR action network from initial source 'root' to joint
    outcomes {(A0,B0), (A0,B1), (A1,B0), (A1,B1)} through local phase/splitter
    actions on A (parameterized by local phase phi_a) and B.

    Demonstrates:
      1. Product source produces rank(C_ij) == 1; entangled pair source produces rank(C_ij) == 2.
      2. No-signalling: varying local action phase `phi_a` on subsystem A leaves
         marginal probabilities P(B=0), P(B=1) strictly unchanged!
    """
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    # Source creates joint intermediate states (a0,b0), (a0,b1), (a1,b0), (a1,b1)
    actions: List[Action] = []
    if entangled:
        # Non-factorizable pair creation: (|00> + |11>) / sqrt(2)
        actions.append(Action("src_00", "root", "pre_0_0", inv_sqrt2 + 0j))
        actions.append(Action("src_11", "root", "pre_1_1", inv_sqrt2 + 0j))
    else:
        # Factorizable creation: 1/2 (|00> + |01> + |10> + |11>)
        for ia in (0, 1):
            for ib in (0, 1):
                actions.append(Action(f"src_{ia}{ib}", "root", f"pre_{ia}_{ib}", 0.5 + 0j))

    # Local unitary action on A only (phase shift phi_a on a=1 followed by Hadamard on A)
    for ib in (0, 1):
        for ia in (0, 1):
            phase = cmath.exp(1j * phi_a) if ia == 1 else 1.0 + 0j
            for out_a in (0, 1):
                sign = -1.0 if (ia == 1 and out_a == 1) else 1.0
                w = inv_sqrt2 * phase * sign
                actions.append(
                    Action(
                        f"localA_{ia}->{out_a}_B{ib}",
                        f"pre_{ia}_{ib}",
                        f"out_{out_a}_{ib}",
                        w,
                    )
                )

    model = FiniteActionModel(actions)
    c_mat: List[List[complex]] = [[0j, 0j], [0j, 0j]]
    for oa in (0, 1):
        for ob in (0, 1):
            c_mat[oa][ob] = model.transition_amplitude("root", f"out_{oa}_{ob}", exact_depth=2)

    rank_c = matrix_rank(c_mat)
    p_b0 = abs(c_mat[0][0]) ** 2 + abs(c_mat[1][0]) ** 2
    p_b1 = abs(c_mat[0][1]) ** 2 + abs(c_mat[1][1]) ** 2
    return {
        "entangled": entangled,
        "rank": rank_c,
        "amplitude_matrix": c_mat,
        "marginal_B0": p_b0,
        "marginal_B1": p_b1,
    }


def build_model_m1(theta: float = math.pi / 3) -> FiniteActionModel:
    """Minimal two-path interference graph with an isolated spacelike action."""
    inv2 = 0.5
    return FiniteActionModel(
        [
            Action("i->a", "i", "a", math.sqrt(inv2) + 0.0j),
            Action("a->f", "a", "f", math.sqrt(inv2) + 0.0j),
            Action("i->b", "i", "b", math.sqrt(inv2) + 0.0j),
            Action("b->f", "b", "f", math.sqrt(inv2) * cmath.exp(1j * theta)),
            Action("x->y", "x", "y", 1.0 + 0.0j),
        ]
    )


def demo() -> None:
    print("=== Model M1: CFR Quantum Action Network ===")
    m1 = build_model_m1(theta=math.pi / 3)
    p_interf = m1.transition_probability("i", "f", exact_depth=2)
    phases = {"i": 0.31, "a": 1.17, "b": -0.42, "f": 0.89, "x": 0.05, "y": -1.20}
    p_gauge = gauge_transform(m1, phases).transition_probability("i", "f", exact_depth=2)
    print(f"Two-path interference P(i->f):        {p_interf:.6f}")
    print(f"After U(1) gauge rephasing P(i->f):   {p_gauge:.6f}")

    for alpha in (1.0, 1.5, 2.0, 3.0):
        res = verify_born_rule_exponent(alpha)
        print(
            f"Born-rule test alpha={alpha:.1f}: two-stage total prob = "
            f"{res['two_stage_total_prob']:.6f} (err={res['conservation_error']:+.6f})"
        )

    b_ent_0 = build_bipartite_action_experiment(entangled=True, phi_a=0.0)
    b_ent_1 = build_bipartite_action_experiment(entangled=True, phi_a=1.234)
    print(f"Entangled bipartite rank:             {b_ent_0['rank']} (>1 => nonfactorizable)")
    print(
        f"No-signalling ΔP(B=0) under local A:  "
        f"{abs(b_ent_0['marginal_B0'] - b_ent_1['marginal_B0']):.2e}"
    )


if __name__ == "__main__":
    demo()
