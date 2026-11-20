# Mathematical Foundations and Proofs of Action Theory (CFR)
## Constraint–Freedom–Roadblock from Pure Action Composition

**Research Status:** Formal axiomatization, mathematical theorems, conditional derivations, and falsifiable experimental protocol within the Constraint–Freedom–Roadblock (CFR) framework.

**Methodological Rule (from `research/research-handoff.md`):**
> *Do **not** count a reinterpretation as a derivation. Do **not** insert GR, QM, the Standard Model, collapse, antigravity, dark matter, or a gauge group by hand and then call them consequences. Classify every ingredient strictly as **Derived**, **Conditionally Derived** (from explicitly stated operational symmetries), **Open**, or **Predicted**.*

---

## Summary Ledger of Epistemic Status

| Target | Result in This Document | Status | Reference |
|---|---|---|---|
| Emergent states $[h]$ without primitive objects | Minimal state space $S_{\mathrm{CFR}} = C/{\sim}$ proved via multi-step continuation congruence $\mathcal{N}^+(h_1) = \mathcal{N}^+(h_2)$ | **Derived (Theorem 2.3)** | §2 |
| Causal ordering $\prec$ and speed limit $c$ | Strict partial order on $C$, spatial antichains, and Kinematic Roadblock outside causal cone | **Derived (Theorems 2.5, 2.7)** | §2 |
| Persistent objects vs. irreversible time | Time = strict progression on irreversible channels; Matter = local periodic orbit $\mathcal{N}_{\mathrm{loc}}^+(\gamma\circ p) = \mathcal{N}_{\mathrm{loc}}^+(p)$ | **Derived (Proposition 2.6)** | §2 |
| Microscopic Freedom Geometry $\mathsf{G}_{AB}(h)$ | Canonical continuation Gram metric on $\mathcal{N}_1(h)$ reducing smoothly to the Fubini–Study metric | **Derived (Definition 3.1, Prop. 3.5)** | §3 |
| Gauge invariance of $\mathsf{G}_{AB}$ and $\mathcal{V}_F$ | $\mathsf{G}_{AB}^{(L)}(h)$ and $\mathcal{V}_F = \sqrt{\det\mathsf{G}}$ are identically invariant under local $U(1)$ and $U(n)$ action rephasings | **Derived (Theorem 3.2)** | §3 |
| Unification of Hard and Soft Roadblocks | $\det\mathsf{G}^{(L)}(h) = 0 \iff$ hard closure ($\mathcal{N}_1 = \varnothing$), future collinearity, or destructive interference extinction | **Derived (Theorem 3.4)** | §3 |
| Complex amplitudes $Z \in \mathbb{C}$ | Forced over $\mathbb{R}$ and $\mathbb{H}$ by Frobenius's division-algebra theorem + continuous reversible interference + subsystem commutativity | **Conditionally Derived (Theorem 4.1)** | §4 |
| Born probability rule $P = |K|^2$ | Unique exponent $\alpha = 2$ in $P(z) = |z|^\alpha$ proved via two-stage symmetric CFR interference conservation | **Conditionally Derived (Theorem 4.2)** | §4 |
| Lorentzian signature $(-,+,\dots,+)$ & $E_0 = mc^2$ | Proper-tick functional $\tau = 2\sqrt{N_+ N_-} = \sqrt{T^2 - X^2/c^2}$ forced by Roadblock vanishing + boost/homogeneity invariance | **Conditionally Derived (Theorem 5.2)** | §5 |
| Macroscopic dimension $d = 3+1$ | Indefinite $(1,d)$ signature is forced; fixing $d = 3$ uniquely from $(\mathfrak{A},\circ)$ remains open (dynamical/topological stability constraints noted) | **Open** | §5.3 |
| Non-Abelian $U(n)$ gauge curvature | Emerges automatically as parallel transport across $n$-fold continuation-degenerate state fibers $[h]$ | **Derived for $U(n)$ (Theorem 6.1)** | §6 |
| Specific gauge group $SU(3)\times SU(2)\times U(1)$ & SM spectrum | Selecting $(3,2,1)$ and chiral fermion representations from a single microscopic $(\mathfrak{A},\circ)$ | **Open** | §6.3 |
| Threshold quantum decoherence $\Gamma_F \mathcal{D}[\rho]$ | Exact GKSL/Lindblad generator derived by tracing amplitudes leaked into Roadblocked ($\mathcal{N}_1 = \varnothing$) sink channels | **Derived (Theorem 7.1)** | §7.1 |
| Gravitational Roadblock defect $\mathcal{K}_{\mu\nu}[\mathsf{G}]$ | Covariantly conserved tensor $\mathcal{K}_{\mu\nu}$ derived by varying the $GL(n,\mathbb{C})/U(n)$ geometric functional of $\mathsf{G}_{AB}(x)$; vanishes for uniform $\mathsf{G}$ and diverges as $\det\mathsf{G} \to 0$ | **Derived (Theorem 7.3)** | §7.2 |
| Quantitative distinction from QM & mass-collapse | High-rank multi-path interferometry at fixed low mass $m$ tests $\Gamma_F(\operatorname{rank}\mathsf{G})$ vs. $\Gamma_{\mathrm{QM}} = 0$ and $\Gamma_{\mathrm{DP/CSL}} \propto m^2$ | **Predicted (§8)** | §8 |

---

## 1. Axioms of a Pure CFR Action System

We begin with **no** spacetime manifold, Hilbert space, metric tensor, mass, energy, or particle ontology.

### Definition 1.1 (CFR Action System)
A **CFR Action System** is a triple

$$
\mathfrak{S} = (\mathfrak{A}, \circ, C)
$$

satisfying:

1. **Elementary actions ($\mathfrak{A}$):** $\mathfrak{A}$ is a non-empty set of primitive actions.
2. **Formal composition ($\circ$):** Let $\mathfrak{A}^+$ denote the free semigroup of finite non-empty chains (words) $h = \alpha_n \circ \dots \circ \alpha_2 \circ \alpha_1$ ($\alpha_k \in \mathfrak{A}$), read right-to-left ("$\alpha_1$ followed by $\alpha_2 \dots$ followed by $\alpha_n$"), with associative concatenation $(h_3 \circ h_2) \circ h_1 = h_3 \circ (h_2 \circ h_1)$. Let $\mathfrak{A}^* = \mathfrak{A}^+ \cup \{\varepsilon\}$, where $\varepsilon$ is the empty continuation satisfying $\varepsilon \circ h = h \circ \varepsilon = h$.
3. **Admissibility Constraint ($C$):** $C \subseteq \mathfrak{A}^+$ is a non-empty subset of **physically admissible histories** obeying the **Sub-history Closure Axiom**:

$$
\forall h_1, h_2 \in \mathfrak{A}^+:\qquad h_2 \circ h_1 \in C \implies h_1 \in C \;\text{ and }\; h_2 \in C.
\tag{A1}
$$

Axiom (A1) expresses a single physical requirement: a composite history cannot be admissible unless every contiguous stage within it is admissible.

### Definition 1.2 (Constraint, Continuation cones, and Hard Roadblock)
For any admissible history $h \in C$, define:

- **Immediate (1-step) continuations:**
  $$
  \mathcal{N}_1(h) := \{\alpha \in \mathfrak{A} : \alpha \circ h \in C\}.
  $$
- **Horizon-$L$ continuations ($L \ge 1$):**
  $$
  \mathcal{N}_L(h) := \{\gamma \in \mathfrak{A}^L : \gamma \circ h \in C\}.
  $$
- **Full continuation cone:**
  $$
  \mathcal{N}^+(h) := \bigcup_{L \ge 1} \mathcal{N}_L(h) = \{\gamma \in \mathfrak{A}^+ : \gamma \circ h \in C\}.
  $$
- **Hard Roadblock:**
  $$
  R_{\mathrm{hard}}(h) \iff \mathcal{N}_1(h) = \varnothing.
  $$

### Lemma 1.3 (Hard Roadblock Termination)
For every $h \in C$, $\mathcal{N}_1(h) = \varnothing \iff \mathcal{N}^+(h) = \varnothing$.

*Proof.* ($\Leftarrow$) Immediate since $\mathcal{N}_1(h) \subseteq \mathcal{N}^+(h)$. ($\Rightarrow$) Suppose $\gamma = \alpha_L \circ \dots \circ \alpha_1 \in \mathcal{N}^+(h)$ with $L \ge 1$. Then $(\alpha_L \circ \dots \circ \alpha_2) \circ (\alpha_1 \circ h) = \gamma \circ h \in C$. If $L = 1$, $\alpha_1 \circ h \in C$ directly; if $L \ge 2$, Axiom (A1) yields $\alpha_1 \circ h \in C$. In both cases $\alpha_1 \in \mathcal{N}_1(h)$, contradicting $\mathcal{N}_1(h) = \varnothing$. $\blacksquare$

---

## 2. Emergent Ontology: States, Causal Order, and Kinematic Roadblocks

In `research/research-handoff.md`, a state is proposed to be an equivalence class of histories with isomorphic future possibilities: $h_1 \sim h_2 \iff \mathcal{N}(h_1) \cong \mathcal{N}(h_2)$. Here we make this precise and prove why **full continuation cones** $\mathcal{N}^+(h)$ (not 1-step sets $\mathcal{N}_1(h)$) are required for states to evolve deterministically under action composition.

### Proposition 2.1 (Insufficiency of 1-Step Equivalence)
Define $h_1 \sim_1 h_2 \iff \mathcal{N}_1(h_1) = \mathcal{N}_1(h_2)$. In general, $\sim_1$ is **not** preserved under admissible composition: one can have $h_1 \sim_1 h_2$ and $\alpha \in \mathcal{N}_1(h_1)$, yet $\alpha \circ h_1 \nsim_1 \alpha \circ h_2$.

*Proof (Explicit Counterexample).* Let $\mathfrak{A} = \{a, b, c, d\}$ and let $C = \{a, b, c \circ a, c \circ b, d \circ c \circ a\}$ together with its subwords $\{c, d, d \circ c\}$. Check (A1): every factor of every word in $C$ lies in $C$. Now compare $h_1 = a$ and $h_2 = b$:
$$
\mathcal{N}_1(a) = \{c\} = \mathcal{N}_1(b) \implies a \sim_1 b.
$$
Compose both with the admissible action $c$:
$$
\mathcal{N}_1(c \circ a) = \{d\} \neq \varnothing = \mathcal{N}_1(c \circ b).
$$
After $c$, history $c \circ b$ hits a Hard Roadblock whereas $c \circ a$ remains open. Hence $\sim_1$ fails to define a self-contained state. $\blacksquare$

### Definition 2.2 (CFR Future Equivalence)
Two admissible histories $h_1, h_2 \in C$ are **future-equivalent** (written $h_1 \sim h_2$) iff their full admissible continuation cones coincide:

$$
h_1 \sim h_2 \iff \mathcal{N}^+(h_1) = \mathcal{N}^+(h_2).
$$

### Theorem 2.3 (Emergent State Space & Minimal Realization — Myhill–Nerode Theorem for CFR)
Let $(\mathfrak{A}, \circ, C)$ be a CFR Action System. Then:

1. $\sim$ is an equivalence relation on $C$.
2. **Left-congruence:** If $h_1 \sim h_2$ and $\alpha \in \mathcal{N}_1(h_1)$, then $\alpha \in \mathcal{N}_1(h_2)$ and $\alpha \circ h_1 \sim \alpha \circ h_2$.
3. **Well-defined emergent state dynamics:** On the quotient **CFR state space** $S_{\mathrm{CFR}} := C / {\sim} = \{[h] : h \in C\}$, every action $\alpha \in \mathfrak{A}$ induces a well-defined partial transition map $\hat{\alpha} : S_{\mathrm{CFR}} \rightharpoonup S_{\mathrm{CFR}}$ given by
   $$
   \hat{\alpha}([h]) := [\alpha \circ h] \qquad \text{whenever } \alpha \in \mathcal{N}_1(h),
   $$
   and $\mathcal{N}_1([h]) := \mathcal{N}_1(h)$, $\mathcal{N}^+([h]) := \mathcal{N}^+(h)$, and $R_{\mathrm{hard}}([h]) := R_{\mathrm{hard}}(h)$ are well-defined invariants of the state $[h]$.
4. **Universal Minimality:** If $(S, \sigma : C \to S, \{\tau_\alpha\}_{\alpha\in\mathfrak{A}})$ is *any* state representation of $C$ such that (i) $\sigma(h)$ determines whether $\alpha \in \mathcal{N}_1(h)$ and (ii) $\sigma(\alpha \circ h) = \tau_\alpha(\sigma(h))$ whenever $\alpha \in \mathcal{N}_1(h)$, then there exists a unique surjective state-homomorphism $\pi : \sigma(C) \twoheadrightarrow S_{\mathrm{CFR}}$ with $\pi(\sigma(h)) = [h]$.

*Proof.*
1. Equality of subsets of $\mathfrak{A}^+$ is reflexive, symmetric, and transitive.
2. Suppose $h_1 \sim h_2$ and $\alpha \in \mathcal{N}_1(h_1)$. Since $\mathcal{N}_1(h) = \mathcal{N}^+(h) \cap \mathfrak{A}$, we immediately obtain $\alpha \in \mathcal{N}_1(h_2)$, so $\alpha \circ h_1, \alpha \circ h_2 \in C$. For any chain $\gamma \in \mathfrak{A}^+$:
   $$
   \gamma \in \mathcal{N}^+(\alpha \circ h_1)
   \iff \gamma \circ (\alpha \circ h_1) \in C
   \iff (\gamma \circ \alpha) \circ h_1 \in C
   \iff \gamma \circ \alpha \in \mathcal{N}^+(h_1).
   $$
   Since $\mathcal{N}^+(h_1) = \mathcal{N}^+(h_2)$, the right-hand side holds iff $\gamma \circ \alpha \in \mathcal{N}^+(h_2) \iff \gamma \in \mathcal{N}^+(\alpha \circ h_2)$. Thus $\mathcal{N}^+(\alpha \circ h_1) = \mathcal{N}^+(\alpha \circ h_2)$, proving $\alpha \circ h_1 \sim \alpha \circ h_2$.
3. Immediate from (2).
4. Suppose $\sigma(h_1) = \sigma(h_2)$. By induction on word length $|\gamma| \ge 1$, assumption (i)–(ii) implies $\gamma \in \mathcal{N}^+(h_1) \iff \gamma \in \mathcal{N}^+(h_2)$: for $|\gamma|=1$ this is (i); if $\gamma = \gamma' \circ \alpha$ has length $L+1$, then $\alpha \in \mathcal{N}_1(h_1) \iff \alpha \in \mathcal{N}_1(h_2)$, and $\sigma(\alpha \circ h_1) = \tau_\alpha(\sigma(h_1)) = \tau_\alpha(\sigma(h_2)) = \sigma(\alpha \circ h_2)$, so by the inductive hypothesis $\gamma' \in \mathcal{N}^+(\alpha \circ h_1) \iff \gamma' \in \mathcal{N}^+(\alpha \circ h_2)$. Hence $\sigma(h_1) = \sigma(h_2) \implies h_1 \sim h_2$, so $\pi(\sigma(h)) := [h]$ is well-defined, surjective, and unique. $\blacksquare$

> **Ontological Corollary:** Physical states do not need to be postulated as primitive containers. They exist canonically as equivalence classes $[h] \in C/{\sim}$ of action histories.

### Definition 2.4 (Causal Order on Histories)
For $h_1, h_2 \in C$, write $h_1 \prec h_2$ iff there exists $\gamma \in \mathfrak{A}^+$ such that $h_2 = \gamma \circ h_1$. Two histories $h_1, h_2 \in C$ are **causally incomparable** (spacelike separated in continuation space) iff $h_1 \nprec h_2$, $h_2 \nprec h_1$, and $h_1 \neq h_2$.

### Theorem 2.5 (Emergent Causal Set Structure)
$(C, \prec)$ is a strict partial order. If $|\mathcal{N}_1(h)| < \infty$ for every $h \in C$, then every causal interval $I(h_1, h_2) := \{h \in C : h_1 \prec h \prec h_2\}$ is finite — i.e., $(C, \prec)$ is a **locally finite causal set** in the sense of Bombelli–Lee–Meyer–Sorkin.

*Proof.* Let $|h| \ge 1$ denote chain length in $\mathfrak{A}^+$.
- *Irreflexivity:* $h = \gamma \circ h \implies |h| = |\gamma| + |h|$ with $|\gamma| \ge 1$, impossible.
- *Transitivity:* If $h_2 = \gamma_1 \circ h_1$ and $h_3 = \gamma_2 \circ h_2$, associativity gives $h_3 = (\gamma_2 \circ \gamma_1) \circ h_1$ with $\gamma_2 \circ \gamma_1 \in \mathfrak{A}^+$ (and $\gamma_2 \circ \gamma_1 \in C$ by (A1)), so $h_1 \prec h_3$.
- *Asymmetry:* Follows from irreflexivity and transitivity.
- *Local finiteness:* If $h_1 \prec h \prec h_2$, then $|h_1| < |h| < |h_2|$. Setting $N = |h_2| - |h_1| \ge 2$, any $h \in I(h_1, h_2)$ has the form $\gamma \circ h_1$ with $1 \le |\gamma| \le N - 1$ and $\gamma \in \mathcal{N}^+(h_1)$. Since each step has finitely many admissible branches $|\mathcal{N}_1(\cdot)| < \infty$, each $\mathcal{N}_k(h_1)$ is finite by induction on $k$, so $I(h_1, h_2) \subseteq \bigcup_{k=1}^{N-1} \{\gamma \circ h_1 : \gamma \in \mathcal{N}_k(h_1)\}$ is finite. $\blacksquare$

### Proposition 2.6 (Time vs. Persistent Matter on the Quotient $S_{\mathrm{CFR}}$)
Induced reachability on states $[h_1] \prec_S [h_2] \iff \exists \gamma \in \mathcal{N}^+(h_1) : [h_2] = [\gamma \circ h_1]$ splits every CFR subsystem into two regimes:
1. **Irreversible (Temporal/Record) Sector:** No non-empty continuation preserves the state ($\forall \gamma \in \mathcal{N}^+(h),\; [\gamma \circ h] \neq [h]$). On this sector, $(S_{\mathrm{CFR}}, \prec_S)$ is a strict partial order defining an irreversible arrow of emergent time.
2. **Periodic (Matter/Clock) Sector:** There exists a minimal cycle $\gamma_0 \in \mathcal{N}^+(h)$ such that $[\gamma_0 \circ h] = [h]$. Then $\gamma_0^n \in \mathcal{N}^+(h)$ for all $n \ge 1$, generating an infinitely persistent state $[h]$ whose cycle count $n$ defines its intrinsic **proper-action tick** $\tau$.

*Proof.* If $[\gamma_0 \circ h] = [h]$, left-congruence (Theorem 2.3(2)) implies $\mathcal{N}^+(\gamma_0^n \circ h) = \mathcal{N}^+(h)$ by induction on $n \ge 1$, so the equivalence class $[h]$ persists indefinitely without any underlying substance. Conversely, absence of state cycles makes $\prec_S$ irreflexive and transitive, hence a strict partial order. $\blacksquare$

### Theorem 2.7 (Kinematic Roadblock / Finite Propagation Speed)
Suppose $\mathfrak{A} = \bigsqcup_{x \in V} \mathfrak{A}_x$ is partitioned over an interaction graph $G_{\mathrm{int}} = (V, E)$ with graph distance $d_G$, such that:
1. Actions on non-adjacent sites commute in state equivalence: if $d_G(x, y) > 1$, then $\alpha_x \circ \alpha_y \sim \alpha_y \circ \alpha_x$ and $\alpha_x \in \mathcal{N}_1(\alpha_y \circ h) \iff \alpha_x \in \mathcal{N}_1(h)$.
2. Admissibility at site $x$ depends only on local and nearest-neighbor history ($d_G(x, y) \le 1$).

Then any constraint modification (intervention) localized at site $x_0$ after history $h$ leaves $\mathcal{N}_L^{(y)}(h)$ completely invariant at every site $y$ satisfying $d_G(x_0, y) > L$. Equivalently, causal influence across $G_{\mathrm{int}}$ cannot exceed $c_{\max} = 1$ graph edge per elementary step; signal propagation channels with $d_G(x_0, y) / L > 1$ encounter an exact **Kinematic Roadblock** ($\Delta \mathcal{N} = \varnothing$).

*Proof.* By induction on $L \ge 1$. For $L = 1$, assumption (2) says admissibility of $\alpha_y \in \mathfrak{A}_y$ depends only on sites at distance $\le 1$ from $y$; if $d_G(x_0, y) > 1$, an intervention at $x_0$ does not alter $\mathcal{N}_1^{(y)}(h)$. For the inductive step $L \to L+1$, if $d_G(x_0, y) > L+1$, every neighbor $z$ of $y$ satisfies $d_G(x_0, z) \ge d_G(x_0, y) - 1 > L$ by the triangle inequality. By the inductive hypothesis, all length-$L$ admissible continuations within the unit neighborhood $B_1(y)$ are unaltered by the intervention at $x_0$, and by assumption (1)–(2) step $L+1$ at $y$ depends only on $B_1(y)$. Thus $\mathcal{N}_{L+1}^{(y)}(h)$ is invariant. $\blacksquare$

---

## 3. Canonical Freedom Geometry $\mathsf{G}_{AB}$, Gauge Invariance, and Roadblocks

`research/research-handoff.md` identifies the Freedom Geometry $\mathsf{G}_{AB}$ and Freedom Volume $\mathcal{V}_F = \sqrt{|\det\mathsf{G}|}$ as *"the main genuinely new CFR object"*, with Roadblocks signaled by $\det\mathsf{G} = 0$ or rank drops, but leaves the microscopic definition of $\mathsf{G}_{AB}$ open. We now construct $\mathsf{G}_{AB}$ canonically from $(\mathfrak{A}, \circ, C, Z)$ and prove its gauge invariance and rank properties.

### Definition 3.1 (Microscopic Continuation Vectors and Freedom Metric)
Let $(\mathfrak{A}, \circ, C)$ be equipped with a multiplicative amplitude map $Z : C \to \mathbb{C}$ satisfying $Z(\beta \circ \alpha) = Z(\beta) Z(\alpha)$ on composable transitions between states in $S_{\mathrm{CFR}}$. Fix an admissible history $h \in C$ with immediate admissible branches $\mathcal{N}_1(h) = \{\alpha_1, \dots, \alpha_k\}$ and horizon $L \ge 1$.

For each branch $\alpha_A \in \mathcal{N}_1(h)$ ($A \in \{1,\dots,k\}$) and each reachable state $x \in S_{\mathrm{CFR}}$, define the **horizon-$L$ continuation amplitude**

$$
\Psi_A^{(L)}(x \mid h) := \sum_{\substack{\gamma \in \mathfrak{A}^{L-1} \\ \gamma \circ \alpha_A \circ h \in C \\ [\gamma \circ \alpha_A \circ h] = x}} Z(\gamma \circ \alpha_A),
\tag{3.1}
$$

where for $L = 1$, $\mathfrak{A}^0 = \{\varepsilon\}$ and $\Psi_A^{(1)}(x \mid h) = Z(\alpha_A)\,\delta_{[\alpha_A \circ h],\, x}$.

The **horizon-$L$ Freedom Geometry** at $h$ is the $k \times k$ Hermitian Gram matrix on $\mathcal{N}_1(h)$:

$$
\mathsf{G}_{AB}^{(L)}(h) := \langle \Psi_A^{(L)}(h) \mid \Psi_B^{(L)}(h) \rangle = \sum_{x \in S_{\mathrm{CFR}}} \overline{\Psi_A^{(L)}(x \mid h)}\, \Psi_B^{(L)}(x \mid h).
\tag{3.2}
$$

Its **effective Freedom dimension** and **Freedom Volume** are:

$$
F_{\mathrm{eff}}^{(L)}(h) := \operatorname{rank}\mathsf{G}^{(L)}(h),
\qquad
\mathcal{V}_F^{(L)}(h) := \begin{cases}
0 & \text{if } \mathcal{N}_1(h) = \varnothing, \\
\sqrt{\det \mathsf{G}^{(L)}(h)} & \text{if } |\mathcal{N}_1(h)| \ge 1.
\end{cases}
\tag{3.3}
$$

*(Note: when $0 \times 0$ matrix conventions set the empty determinant to $1$, CFR explicitly sets $\mathcal{V}_F = 0$ on $\mathcal{N}_1(h) = \varnothing$ because zero continuation channels enclose zero freedom volume; for $|\mathcal{N}_1(h)| \ge 1$, $\mathsf{G}^{(L)} = \Psi^\dagger \Psi \succeq 0$ guarantees $\det\mathsf{G}^{(L)}(h) \in \mathbb{R}_{\ge 0}$ automatically.)*

### Theorem 3.2 (Exact Local Gauge Invariance of $\mathsf{G}_{AB}$ and $\mathcal{V}_F$)
Let $\theta : S_{\mathrm{CFR}} \to \mathbb{R}$ be an arbitrary state-dependent phase function, and transform every elementary action $\beta : u \to v$ between states $u, v \in S_{\mathrm{CFR}}$ by the local $U(1)$ gauge transformation

$$
Z'(\beta) = e^{i\theta(u)}\, Z(\beta)\, e^{-i\theta(v)}.
\tag{3.4}
$$

More generally, if each state $x \in S_{\mathrm{CFR}}$ carries an $n_x$-dimensional internal vector space and $Z(\beta) \in \operatorname{Hom}(\mathbb{C}^{n_u}, \mathbb{C}^{n_v})$ transforms under local unitary gauge maps $V(x) \in U(n_x)$ via $Z'(\beta) = V(v)\, Z(\beta)\, V(u)^\dagger$, with $\mathsf{G}_{AB}^{(L)}(h) = \sum_x \operatorname{Tr}\!\left(\Psi_A^{(L)}(x\mid h)^\dagger \Psi_B^{(L)}(x\mid h)\right)$ on a fixed initial unit frame, then for **every** $h \in C$ and **every** horizon $L \ge 1$:

$$
\mathsf{G}_{AB}^{\prime\,(L)}(h) = \mathsf{G}_{AB}^{(L)}(h),
\qquad
F_{\mathrm{eff}}^{\prime\,(L)}(h) = F_{\mathrm{eff}}^{(L)}(h),
\qquad
\mathcal{V}_F^{\prime\,(L)}(h) = \mathcal{V}_F^{(L)}(h).
\tag{3.5}
$$

*Proof.* Let $u_0 = [h]$. Along any $L$-step path $p = \beta_L \circ \dots \circ \beta_2 \circ \alpha_A$ from $u_0 = [h]$ through intermediate states $u_1, \dots, u_{L-1}$ to $u_L = x$, internal phases/unitaries telescope at every intermediate state:
$$
Z'(p) = \left(V(u_L) Z(\beta_L) V(u_{L-1})^\dagger\right) \cdots \left(V(u_1) Z(\alpha_A) V(u_0)^\dagger\right) = V(x)\, Z(p)\, V(u_0)^\dagger
$$
(in the Abelian $U(1)$ case, $Z'(p) = e^{i\theta(u_0)} Z(p) e^{-i\theta(x)}$). Summing over all paths reaching $x$ gives $\Psi_A^{\prime\,(L)}(x \mid h) = V(x)\,\Psi_A^{(L)}(x \mid h)\,V(u_0)^\dagger$ (Abelian: $e^{i\theta(u_0)}\Psi_A^{(L)}(x \mid h)e^{-i\theta(x)}$). Substituting into (3.2):

- **Abelian $U(1)$ case:**
  $$
  \mathsf{G}_{AB}^{\prime\,(L)}(h)
  = \sum_{x \in S_{\mathrm{CFR}}} e^{-i\theta(u_0)} e^{i\theta(x)} \overline{\Psi_A^{(L)}(x \mid h)}\, e^{i\theta(u_0)} e^{-i\theta(x)} \Psi_B^{(L)}(x \mid h)
  = \sum_{x \in S_{\mathrm{CFR}}} \overline{\Psi_A^{(L)}(x \mid h)}\, \Psi_B^{(L)}(x \mid h)
  = \mathsf{G}_{AB}^{(L)}(h).
  $$
- **Non-Abelian $U(n)$ trace metric:** By cyclicity of trace and $V(x)^\dagger V(x) = I_{n_x}$, $V(u_0)^\dagger V(u_0) = I_{n_{u_0}}$:
  $$
  \sum_x \operatorname{Tr}\!\left(V(u_0)\Psi_A^{(L)}(x\mid h)^\dagger V(x)^\dagger V(x) \Psi_B^{(L)}(x\mid h) V(u_0)^\dagger\right)
  = \sum_x \operatorname{Tr}\!\left(\Psi_A^{(L)}(x\mid h)^\dagger \Psi_B^{(L)}(x\mid h)\right).
  $$
Since every matrix entry of $\mathsf{G}^{(L)}(h)$ is strictly invariant, its rank and determinant are strictly invariant. $\blacksquare$

### Theorem 3.4 (The Roadblock Rank Theorem)
For any $h \in C$ and horizon $L \ge 1$, the Freedom Volume vanishes ($\mathcal{V}_F^{(L)}(h) = 0$) if and only if at least one of the following three physical mechanisms occurs:

1. **Hard Roadblock ($\mathcal{N}_1(h) = \varnothing$):** All outgoing action channels are forbidden by constraints $C$ ($F_{\mathrm{eff}} = 0$).
2. **Interference Roadblock ($\Psi_A^{(L)}(\cdot \mid h) \equiv 0$ for some $\alpha_A \in \mathcal{N}_1(h)$):** Branch $\alpha_A$ is 1-step admissible, but its horizon-$L$ continuations interfere destructively to zero at every reachable state $x$, producing a zero row/column in $\mathsf{G}^{(L)}(h)$.
3. **Collinear / Merging Roadblock ($\sum_{A=1}^k c_A \Psi_A^{(L)}(\cdot \mid h) = 0$ with $\ge 2$ nonzero $c_A$):** Distinct initial actions $\alpha_A \neq \alpha_B$ collapse onto linearly dependent future state distributions, dropping the continuation rank strictly below $|\mathcal{N}_1(h)|$:
   $$
   F_{\mathrm{eff}}^{(L)}(h) = \operatorname{rank}\mathsf{G}^{(L)}(h) < |\mathcal{N}_1(h)|.
   $$

*Proof.* If $\mathcal{N}_1(h) = \varnothing$, $\mathcal{V}_F^{(L)}(h) = 0$ by (3.3). Suppose $|\mathcal{N}_1(h)| = k \ge 1$, and arrange the vectors $\{\Psi_A^{(L)}(\cdot \mid h)\}_{A=1}^k$ as columns of a matrix $M$. Then $\mathsf{G}^{(L)}(h) = M^\dagger M$. By elementary linear algebra over $\mathbb{C}$, $\ker(M^\dagger M) = \ker(M)$: if $M^\dagger M c = 0$, then $c^\dagger M^\dagger M c = \|Mc\|_2^2 = 0 \implies Mc = 0$, and conversely. Hence $\det\mathsf{G}^{(L)}(h) = 0 \iff \ker(M) \neq \{0\} \iff \operatorname{rank}\mathsf{G}^{(L)}(h) < k$. A non-zero vector $c \in \ker(M)$ either has support of size $1$ (giving $\Psi_A^{(L)} \equiv 0$, Case 2) or support of size $\ge 2$ (giving non-trivial linear dependence among nonzero continuation vectors, Case 3). $\blacksquare$

### Proposition 3.5 (Continuum Limit = Fubini–Study Quantum Metric)
Suppose admissible continuations from $h$ form a smooth manifold $M_h$ parameterized by real coordinates $\theta = (\theta^1, \dots, \theta^m)$, with non-vanishing continuation state $|\Psi(\theta; h)\rangle$ and normalized continuation ray $|\psi(\theta)\rangle := |\Psi(\theta; h)\rangle / \|\Psi(\theta; h)\|$. Then the local gauge-invariant distinguishability of infinitesimally separated continuations $\theta$ and $\theta + d\theta$,
$$
ds_F^2 := 1 - \left|\langle \psi(\theta) \mid \psi(\theta + d\theta) \rangle\right|^2 = \mathsf{G}_{ab}^{\mathrm{FS}}(h;\theta)\, d\theta^a d\theta^b + O(\|d\theta\|^3),
$$
defines the **Fubini–Study metric**
$$
\mathsf{G}_{ab}^{\mathrm{FS}}(h;\theta) = \operatorname{Re}\!\left[\langle \partial_a \psi \mid \partial_b \psi \rangle - \langle \psi \mid \partial_a \psi \rangle \langle \partial_b \psi \mid \psi \rangle\right],
\tag{3.6}
$$
which is invariant under smooth continuation-dependent phase gauge transformations $|\psi(\theta)\rangle \mapsto e^{i\chi(\theta)}|\psi(\theta)\rangle$.

*Proof.* Expand $|\psi(\theta + d\theta)\rangle = |\psi\rangle + \partial_a |\psi\rangle d\theta^a + \frac{1}{2}\partial_a\partial_b|\psi\rangle d\theta^a d\theta^b + O(\|d\theta\|^3)$. Differentiating $\langle\psi\mid\psi\rangle = 1$ twice gives $\langle\psi\mid\partial_a\psi\rangle + \langle\partial_a\psi\mid\psi\rangle = 0$ (so $\langle\psi\mid\partial_a\psi\rangle = i A_a$ is purely imaginary) and $\operatorname{Re}\langle\psi\mid\partial_a\partial_b\psi\rangle = -\operatorname{Re}\langle\partial_a\psi\mid\partial_b\psi\rangle$. Computing $|\langle\psi(\theta)\mid\psi(\theta+d\theta)\rangle|^2 = \left|1 + i A_a d\theta^a + \frac{1}{2}\langle\psi\mid\partial_a\partial_b\psi\rangle d\theta^a d\theta^b + \dots\right|^2 = 1 + (iA_a - iA_a)d\theta^a + \left(\operatorname{Re}\langle\psi\mid\partial_a\partial_b\psi\rangle + A_a A_b\right)d\theta^a d\theta^b + O(\|d\theta\|^3) = 1 - \left(\operatorname{Re}\langle\partial_a\psi\mid\partial_b\psi\rangle - \langle\psi\mid\partial_a\psi\rangle\langle\partial_b\psi\mid\psi\rangle\right)d\theta^a d\theta^b + O(\|d\theta\|^3)$ yields (3.6). Under $|\psi'\rangle = e^{i\chi}|\psi\rangle$, $|\langle\psi'(\theta)\mid\psi'(\theta+d\theta)\rangle| = |e^{-i\chi(\theta)} e^{i\chi(\theta+d\theta)}|\cdot|\langle\psi(\theta)\mid\psi(\theta+d\theta)\rangle| = |\langle\psi(\theta)\mid\psi(\theta+d\theta)\rangle|$, so (3.6) is gauge-invariant. $\blacksquare$

---

## 4. Conditional Derivation of Complex Amplitudes and Born's Rule

Per CFR's Research Principle, one cannot obtain $\mathbb{C}$ and $P = |K|^2$ from set theory alone without stating how parallel and serial action channels combine. What *can* be proved rigorously is that **five minimal operational axioms on CFR action composition uniquely force $\mathbb{C}$ and the exponent $2$ in $P = |K|^2$**, ruling out $\mathbb{R}$, $\mathbb{H}$, and every $P = |K|^\alpha$ with $\alpha \neq 2$.

### Axioms for CFR Action Valuations
Let $(\mathbb{A}, +, \cdot)$ be a finite-dimensional associative algebra over $\mathbb{R}$ with unit $1 = Z(\varepsilon)$, assigning an amplitude $Z(\gamma) \in \mathbb{A}$ to admissible paths and a continuous transition weight $P : \mathbb{A} \to \mathbb{R}_{\ge 0}$ satisfying:

- **(V1) Serial Multiplicativity:** $Z(\gamma_2 \circ \gamma_1) = Z(\gamma_2) Z(\gamma_1)$, and for unbranched serial composition, $P(z_2 z_1) = P(z_2) P(z_1)$ with $P(1) = 1$ and $P(0) = 0$.
- **(V2) Parallel Additivity:** Two distinct admissible paths $\gamma_1, \gamma_2$ sharing start and end states combine as $Z(\gamma_1 \oplus \gamma_2) = Z(\gamma_1) + Z(\gamma_2)$, distributing over $\circ$.
- **(V3) Non-Degeneracy of Open Channels:** Every non-zero amplitude has positive weight ($z \neq 0 \iff P(z) > 0$).
- **(V4) Continuous Reversible Phase Symmetry:** The unit-weight group $U(\mathbb{A}) := \{u \in \mathbb{A} : P(u) = 1\}$ is path-connected and contains elements $u_1, u_2 \in U(\mathbb{A})$ capable of exact destructive interference ($u_1 + u_2 = 0$ achieved along a continuous curve in $U(\mathbb{A})$).
- **(V5) Commutative Spacelike Composition:** If $\alpha_A \in \mathfrak{A}_A$ and $\alpha_B \in \mathfrak{A}_B$ act on causally independent subsystems ($\alpha_A \circ \alpha_B \sim \alpha_B \circ \alpha_A$), their joint amplitude satisfies $Z(\alpha_A \circ \alpha_B) = Z(\alpha_A) Z(\alpha_B) = Z(\alpha_B) Z(\alpha_A)$.

### Theorem 4.1 (Uniqueness of Complex Amplitudes $\mathbb{A} \cong \mathbb{C}$)
Any finite-dimensional real associative valuation algebra $(\mathbb{A}, P)$ satisfying (V1)–(V5) is isomorphic as an $\mathbb{R}$-algebra to $\mathbb{C}$.

*Proof.*
1. **No zero divisors:** If $z_1 \neq 0$ and $z_2 \neq 0$, (V3) gives $P(z_1) > 0$ and $P(z_2) > 0$; (V1) gives $P(z_1 z_2) = P(z_1) P(z_2) > 0$; (V3) then implies $z_1 z_2 \neq 0$.
2. **Frobenius Division-Algebra Classification:** A finite-dimensional associative $\mathbb{R}$-algebra with $1$ and no zero divisors is a division algebra: for every $z \neq 0$, left-multiplication $L_z : \mathbb{A} \to \mathbb{A}$ is $\mathbb{R}$-linear and injective, hence surjective since $\dim_\mathbb{R}\mathbb{A} < \infty$, so $z^{-1} \in \mathbb{A}$ exists. By **Frobenius's Theorem (1877)**, $\mathbb{A}$ is isomorphic to $\mathbb{R}$, $\mathbb{C}$, or the quaternions $\mathbb{H}$.
3. **Exclusion of $\mathbb{R}$:** For $\mathbb{A} = \mathbb{R}$, $P(1) = 1$ and $P((-1)^2) = P(-1)^2 \implies P(-1) = 1$, while for $|r| \neq 1$, $P(r^n) = P(r)^n$ diverges or vanishes unless $P(r)=1$, which contradicts continuity and $P(0)=0$ as $r \to 0$. Thus $U(\mathbb{R}) = \{+1, -1\}$ is disconnected (0-dimensional), violating (V4): one cannot continuously tune an action phase from $+1$ to $-1$ without passing through $0$ (closing the channel).
4. **Exclusion of $\mathbb{H}$:** Since independent subsystems can execute arbitrary single-channel amplitudes $q_A, q_B \in \mathbb{A}$ spacelike-independently, (V5) requires $q_A q_B = q_B q_A$ for all realizable amplitudes generating $\mathbb{A}$. Thus $\mathbb{A}$ is commutative, excluding $\mathbb{H}$ ($ij = -ji \neq ji$).
5. Only $\mathbb{A} \cong \mathbb{C}$ survives, where $U(\mathbb{C}) = U(1) = \{e^{i\theta} : \theta \in \mathbb{R}\} \cong S^1$ is connected and $1 + e^{i\pi} = 0$. $\blacksquare$

### Theorem 4.2 (Derivation of Born's Rule $P(z) = |z|^2$)
Let $P : \mathbb{C} \to \mathbb{R}_{\ge 0}$ satisfy (V1)–(V4) together with **Probability Conservation on Closed Reversible Branchings**: whenever a state $i$ has exhaustive, mutually exclusive target states $\{1, \dots, m\}$ with total probability $\sum_{j=1}^m P(K(j,i)) = 1$, composing two such reversible stages preserves total probability $1$ whenever no Hard Roadblock occurs. Then uniquely:

$$
P(z) = |z|^2 \qquad \forall z \in \mathbb{C}.
$$

*Proof.*
1. **Reduction to $P(z) = |z|^\alpha$:** Write $z = r e^{i\theta}$ with $r = |z| \ge 0$ and $\theta \in \mathbb{R}$. For every rational $\theta / (2\pi) = p/q$, $(e^{i\theta})^q = 1 \implies P(e^{i\theta})^q = P(1) = 1 \implies P(e^{i\theta}) = 1$; by continuity of $P$, $P(e^{i\theta}) = 1$ for all $\theta \in \mathbb{R}$. Hence $P(r e^{i\theta}) = P(r) P(e^{i\theta}) = P(r)$. On $\mathbb{R}_{>0}$, $f(t) := \ln P(e^t)$ is continuous and satisfies Cauchy's equation $f(t_1 + t_2) = f(t_1) + f(t_2)$, so $f(t) = \alpha t$ for a constant $\alpha \in \mathbb{R}$, i.e. $P(r) = r^\alpha$. Since $P(0) = 0$ and $P$ is continuous at $0$, $\alpha > 0$. Thus $P(z) = |z|^\alpha$ for some $\alpha > 0$.
2. **Two-stage symmetric interference fixes $\alpha = 2$ (without assuming Hilbert space or $1/\sqrt{2}$):**
   Consider a reversible 2-state symmetric branching gate $G$ on states $\{1, 2\}$ whose four elementary transition amplitudes have equal magnitude $r > 0$:
   $$
   G = \begin{pmatrix} r & r \\ r & -r \end{pmatrix} = r \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}.
   $$
   - **Stage 1 conservation:** Starting at state $1$, the two exhaustive outgoing transitions have amplitudes $G_{11} = r$ and $G_{21} = r$. Probability conservation over exhaustive branches gives:
     $$
     P(G_{11}) + P(G_{21}) = r^\alpha + r^\alpha = 2 r^\alpha = 1 \implies r^\alpha = \frac{1}{2}.
     \tag{4.1}
     $$
     (Symmetrically, starting at state $2$ gives $P(G_{12}) + P(G_{22}) = r^\alpha + |-r|^\alpha = 2 r^\alpha = 1$.)
   - **Stage 2 serial composition ($G \circ G$):** Compose two identical stages in series. By (V1) and (V2), the 2-step transition amplitudes from state $1$ are:
     $$
     K^{(2)}(1 \leftarrow 1) = G_{11} G_{11} + G_{12} G_{21} = r^2 + r^2 = 2 r^2,
     $$
     $$
     K^{(2)}(2 \leftarrow 1) = G_{21} G_{11} + G_{22} G_{21} = r^2 - r^2 = 0 \quad (\text{exact Interference Roadblock on } 1 \to 2).
     $$
   - **Two-stage probability conservation:** Because $P(K^{(2)}(2 \leftarrow 1)) = P(0) = 0$, conservation of total probability across the composed reversible process requires:
     $$
     P\!\left(K^{(2)}(1 \leftarrow 1)\right) + P\!\left(K^{(2)}(2 \leftarrow 1)\right) = (2 r^2)^\alpha + 0 = 1.
     \tag{4.2}
     $$
   Substitute $r^\alpha = \frac{1}{2}$ from (4.1) into (4.2):
   $$
   2^\alpha \left(r^\alpha\right)^2 = 1 \implies 2^\alpha \cdot \frac{1}{4} = 1 \implies 2^{\alpha - 2} = 1 \implies \boxed{\alpha = 2}. \quad \blacksquare
   $$

---

## 5. Derivation of Lorentzian Signature and Completion of $E = mc^2$

In `research/mass-energy-equivalence.md` (§2.2), mass–energy equivalence $E_0 = mc^2$ was derived from action stiffness $\mu$ and Kinematic Roadblock $c$, *assuming* the emergent proper-time interval $d\tau = dt\sqrt{1 - v^2/c^2}$. Here we prove why CFR's causal cone and Kinematic Roadblock force the Lorentzian minus sign $(-,+,\dots,+)$ rather than Euclidean $(+,+,\dots,+)$.

### 5.1 The 1+1 Causal Action Diamond
Consider a localized stable action pattern propagating on a homogeneous 1+1 causal action network where each elementary step advances either along the right-moving causal generator $\alpha_+$ or the left-moving causal generator $\alpha_-$, with commuting parallel displacements $\alpha_+ \circ \alpha_- \sim \alpha_- \circ \alpha_+$.

Across $T = N_+ + N_-$ total elementary steps ($N_+, N_- \in \mathbb{Z}_{\ge 0}$):
- **Emergent temporal depth:** $T = N_+ + N_-$ (counting serial action steps).
- **Net spatial displacement:** $X = c(N_+ - N_-)$ (where $c$ is the 1-hop-per-step Kinematic Roadblock of Theorem 2.7, so $|X| \le cT$, i.e. $|v| := |X/T| \le c$).
- **Boundary Kinematic Roadblocks:**
  - When $N_- = 0$ ($v = +c$), the pattern expends 100% of its steps propagating rightward; zero steps remain to execute the internal cycle $\alpha_- \circ \alpha_+$ that maintains its rest pattern.
  - Symmetrically, when $N_+ = 0$ ($v = -c$), the leftward Kinematic Roadblock is hit.

Notice the exact algebraic identity linking the product of directional continuations to $(T, X)$:

$$
4 N_+ N_- = (N_+ + N_-)^2 - (N_+ - N_-)^2 = T^2 - \frac{X^2}{c^2}.
\tag{5.1}
$$

### Theorem 5.2 (Uniqueness of Lorentzian Proper-Tick Interval)
Let $\tau : \mathbb{R}_{\ge 0}^2 \to \mathbb{R}_{\ge 0}$ be a continuous coarse-grained internal proper-tick functional $\tau(N_+, N_-)$ of a stable CFR pattern satisfying:
1. **Kinematic Roadblock Vanishing:** Internal pattern cycling halts on the null Roadblock boundary: $\tau(N_+, 0) = \tau(0, N_-) = 0$.
2. **Causal Additivity along Uniform Histories (Degree-1 Homogeneity):** Scaling a uniform trajectory by $\lambda \ge 0$ scales accumulated internal ticks linearly: $\tau(\lambda N_+, \lambda N_-) = \lambda\,\tau(N_+, N_-)$.
3. **Spatial Parity & Cone-Automorphism (Boost) Invariance:** $\tau(N_+, N_-) = \tau(N_-, N_+)$, and $\tau$ is invariant under causal-cone-preserving area-preserving rescalings $(N_+, N_-) \mapsto (e^\eta N_+, e^{-\eta} N_-)$ ($\eta \in \mathbb{R}$, the unique connected group of linear automorphisms preserving the future cone $\mathbb{R}_{\ge 0}^2$ up to overall scale).
4. **Rest-Clock Normalization:** At rest ($X = 0$, so $N_+ = N_- = T/2$), $\tau(T/2, T/2) = T$.

Then uniquely:

$$
\tau(N_+, N_-) = 2\sqrt{N_+ N_-} = \sqrt{T^2 - \frac{X^2}{c^2}} = T\sqrt{1 - \frac{v^2}{c^2}}.
\tag{5.2}
$$

In $d$ isotropic spatial dimensions (requiring $SO(d)$ rotational invariance on spatial antichains and reducing to (5.2) along every spatial axis), the unique invariant quadratic line element is Lorentzian with signature $(-, \underbrace{+, \dots, +}_{d})$:

$$
ds^2 = -c^2 d\tau^2 = -c^2 dt^2 + \sum_{i=1}^d (dx^i)^2.
\tag{5.3}
$$

*Proof.* For any $N_+ > 0, N_- > 0$, choose $\eta = \frac{1}{2}\ln(N_- / N_+) \in \mathbb{R}$. Then $e^\eta N_+ = \sqrt{N_+ N_-}$ and $e^{-\eta} N_- = \sqrt{N_+ N_-}$. By boost invariance (3), homogeneity (2), and normalization (4):
$$
\tau(N_+, N_-)
= \tau\!\left(\sqrt{N_+ N_-},\, \sqrt{N_+ N_-}\right)
= 2\sqrt{N_+ N_-}\,\tau\!\left(\tfrac{1}{2},\, \tfrac{1}{2}\right)
= 2\sqrt{N_+ N_-}.
$$
By continuity (or condition 1 directly), this extends to $\tau(N_+, 0) = \tau(0, N_-) = 0$ on the boundary. Substituting $N_\pm = \frac{1}{2}(T \pm X/c)$ yields $\tau = \sqrt{T^2 - X^2/c^2} = T\sqrt{1 - v^2/c^2}$. In $d$ isotropic spatial dimensions, $SO(d)$ invariance requires $\tau(T, \mathbf{X}) = \tilde{\tau}(T, \|\mathbf{X}\|)$, and restricting $\mathbf{X} = (X, 0, \dots, 0)$ to the first axis forces $\tilde{\tau}(T, \|\mathbf{X}\|) = \sqrt{T^2 - \|\mathbf{X}\|^2/c^2}$, which has exactly 1 negative and $d$ positive eigenvalues in $ds^2 = -c^2 d\tau^2$. $\blacksquare$

> **Why Euclidean signature $(+,+,\dots,+)$ is impossible in CFR:** Euclidean rotations mix $T$ and $X$, mapping admissible future chains ($T > 0, X = 0$) into backward chains ($T < 0$), violating the irreversibility of the causal partial order $\prec$ (Theorem 2.5) and erasing the Kinematic Roadblock boundary $|X| = cT$. Thus **1 minus sign = 1 causal composition order $\circ$; $d$ plus signs = $d$ mutually commuting spatial action directions**.

### Corollary 5.3 (Completion of $E = mc^2$ and Relativistic Dispersion)
Combining Theorem 5.2 with `research/mass-energy-equivalence.md` (§2.1–§3.1): a stable periodic CFR pattern of invariant topological stiffness $m := \mu$ has effective action $S = -mc^2 \int d\tau = -mc^2 \int dt\sqrt{1 - \mathbf{v}^2/c^2}$, canonical momentum $\mathbf{p} = \frac{\partial L}{\partial \mathbf{v}} = \frac{m\mathbf{v}}{\sqrt{1 - \mathbf{v}^2/c^2}}$, and Noether time-translation invariant
$$
E = \mathbf{p}\cdot\mathbf{v} - L = \frac{mc^2}{\sqrt{1 - \mathbf{v}^2/c^2}},
\qquad
E^2 = \mathbf{p}^2 c^2 + m^2 c^4,
\qquad
E_0 = mc^2.
$$

### 5.3 Honest Status of $d = 3$ Spatial Dimensions (Open Problem)
Theorem 5.2 derives the **Lorentzian signature $(-,+,\dots,+)$** for any $d \ge 1$, but does **not** by itself force $d = 3$. In CFR, $d = 3$ is constrained heuristically by stable-knot ontology ("matter = stable localized action knot"): topological 1D loops trivialize in $d \ge 4$ (any closed 1-manifold unknots smoothly in $\mathbb{R}^d$ for $d \ge 4$, and inverse-power bound states destabilize for $d \ge 4$), whereas $d \le 2$ restricts worldline exchange to braid groups rather than symmetric boson/fermion statistics $S_N$. Deriving $d = 3$ unconditionally as the unique infrared fixed point of a microscopic $(\mathfrak{A}, \circ, C)$ graph growth law remains **Open**.

---

## 6. Non-Abelian $U(n)$ Gauge Curvature from Continuation Degeneracy

In `research/research-handoff.md`, $U(1)$ link variables were posited by hand. Using Theorem 3.2, we now show that **non-Abelian $U(n)$ Yang–Mills connections arise automatically** whenever a CFR state $[h]$ possesses $n$-fold internal continuation symmetry.

### Theorem 6.1 (Emergence of Non-Abelian $U(n)$ Gauge Connections)
Suppose at each coarse-grained site $x$, the local state space splits into $n$ internal sub-histories $\{h_x^{(1)}, \dots, h_x^{(n)}\}$ whose external continuation cones are isomorphic and orthonormal in Freedom Geometry:

$$
\mathsf{G}_{ab}^{\mathrm{int}}(x) = \langle \Psi(h_x^{(a)}) \mid \Psi(h_x^{(b)}) \rangle = \delta_{ab} \qquad (a, b \in \{1,\dots,n\}).
$$

Then:
1. **Local $U(n)$ Redundancy:** At each site $x$, rotating the internal basis by any unitary matrix $V(x) \in U(n)$ preserves $\mathsf{G}^{\mathrm{int}}(x) = V(x) I_n V(x)^\dagger = I_n$ and all external continuation invariants.
2. **Matrix Link Variables & Parallel Transport:** Any elementary inter-site action channel $x \to y$ preserving continuation norm induces an $n \times n$ unitary transport matrix $U_{yx} \in U(n)$ transforming covariantly as
   $$
   U_{yx} \;\longmapsto\; V(y)\, U_{yx}\, V(x)^\dagger.
   \tag{6.1}
   $$
3. **Gauge-Invariant Plaquette Action & Yang–Mills Continuum Limit:** Around any elementary closed 4-cycle (plaquette) $\square = (x \to y \to z \to w \to x)$, the holonomy $U_\square := U_{xw} U_{wz} U_{zy} U_{yx}$ transforms by conjugation $U_\square \mapsto V(x) U_\square V(x)^\dagger$, so the real trace
   $$
   S_{\square}[U] = \beta_g \left(n - \operatorname{Re}\operatorname{Tr} U_\square\right)
   \tag{6.2}
   $$
   is strictly locally $U(n)$-invariant. Writing $U_{x+\epsilon\hat{\mu},\,x} = \exp\!\left(i g \epsilon A_\mu(x)\right)$ with Hermitian $A_\mu = A_\mu^A T_A \in \mathfrak{u}(n)$ and lattice spacing $\epsilon \to 0$ yields
   $$
   U_\square = \exp\!\left(i g \epsilon^2 F_{\mu\nu} + O(\epsilon^3)\right),
   \qquad
   F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu - i g [A_\mu, A_\nu],
   \tag{6.3}
   $$
   and $\sum_\square S_\square \to \frac{1}{2g^2_{\mathrm{eff}}} \int d^4x\, \operatorname{Tr}(F_{\mu\nu} F^{\mu\nu})$ by the Baker–Campbell–Hausdorff expansion.

*Proof.* (1) follows from $V(x)^\dagger V(x) = I_n$. (2) follows because $U_{yx}$ represents a linear norm-preserving action map from fiber $\mathbb{C}^n_x$ to $\mathbb{C}^n_y$, changing basis at $x$ by $V(x)$ and at $y$ by $V(y)$. (3) Cyclicity of trace gives $\operatorname{Tr}(V(x) U_\square V(x)^\dagger) = \operatorname{Tr}(U_\square)$. For $\square$ in the $(\mu,\nu)$ plane, BCH gives $\ln(e^{ig\epsilon A_\mu(x+\epsilon\hat{\nu})\text{ path}}) = ig\epsilon^2(\partial_\mu A_\nu - \partial_\nu A_\mu - ig[A_\mu, A_\nu]) + O(\epsilon^3) = ig\epsilon^2 F_{\mu\nu} + O(\epsilon^3)$. Expanding $n - \operatorname{Re}\operatorname{Tr}(I_n + ig\epsilon^2 F_{\mu\nu} - \frac{1}{2}g^2\epsilon^4 F_{\mu\nu}^2 + O(\epsilon^5))$ uses $\operatorname{Re}\operatorname{Tr}(i F_{\mu\nu}) = 0$ (since $F_{\mu\nu}$ is Hermitian), leaving $\frac{1}{2}\beta_g g^2 \epsilon^4 \operatorname{Tr}(F_{\mu\nu}^2)$ per plaquette. $\blacksquare$

### 6.3 Honest Status of $SU(3)\times SU(2)\times U(1)$ (Open Problem)
Theorem 6.1 derives *why internal continuation degeneracies produce Yang–Mills gauge fields*, without inserting gauge fields by hand. However, deriving **why** the vacuum action network exhibits specifically $n = 3$, $n = 2$ (chiral), and $n = 1$ degenerate fibers — and deriving the 3-generation fermion mass ratios — remains **Open**.

---

## 7. Microscopic Derivation of New CFR Physics at Roadblocks

`research/research-handoff.md` proposes two candidate signatures where CFR departs from standard QM and GR at Roadblocks:
1. A threshold quantum master equation $\frac{d\rho}{dt} = -\frac{i}{\hbar}[H,\rho] + \Gamma_F \mathcal{D}_Q[\rho]$ with $\Gamma_F = 0$ in regular regimes.
2. A gravitational correction $G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu} + \lambda_F \mathcal{K}_{\mu\nu}[\mathfrak{A}]$ vanishing when Freedom Geometry is regular/uniform and activating when Freedom Geometry becomes strongly distorted or approaches $\det\mathsf{G} = 0$.

We now **derive both structures microscopically** from CFR's continuation rules rather than postulating them.

### 7.1 Quantum Roadblock Decoherence from Channel Closure

Consider an effective quantum state space $\mathcal{H}_{\mathrm{reg}}$ describing regular, reversible action channels ($\mathcal{V}_F > 0$). Suppose at a structural threshold (either $\det\mathsf{G}(h) \to 0$ or when continuation branching rank $R_F = \operatorname{rank}\mathsf{G}$ exceeds a finite constraint-coherence rank $R_c$), step evolution over $\Delta t$ couples $\mathcal{H}_{\mathrm{reg}}$ to $m = \max(0,\, R_F - R_c)$ **Roadblocked sink channels** $\{|r_k\rangle\}_{k=1}^m \subset \mathcal{H}_{\mathrm{RB}}$ satisfying $\mathcal{N}_1(|r_k\rangle) = \varnothing$ (no return continuations back into $\mathcal{H}_{\mathrm{reg}}$; each $|r_k\rangle$ terminates its coherent phase branch and records an irreversible boundary event).

### Theorem 7.1 (Microscopic Threshold Lindblad Master Equation)
Let single-step CFR evolution on $\mathcal{H}_{\mathrm{reg}} \oplus \mathcal{H}_{\mathrm{RB}}$ from an initial regular density state $\rho \oplus 0$ act via a norm-preserving transition $V_{\Delta t} : \mathcal{H}_{\mathrm{reg}} \to \mathcal{H}_{\mathrm{reg}} \oplus \mathcal{H}_{\mathrm{RB}}$:

$$
V_{\Delta t}|\psi\rangle = \left(I - \frac{i}{\hbar} H \Delta t - \frac{\Delta t}{2}\sum_{k=1}^m L_k^\dagger L_k\right)|\psi\rangle \oplus \bigoplus_{k=1}^m \sqrt{\Delta t}\, L_k |\psi\rangle + O(\Delta t^{3/2}),
\tag{7.1}
$$

where $L_k = 0$ identically whenever $m = 0$ (no Roadblocked channels reachable). Because $\mathcal{N}_1(|r_k\rangle) = \varnothing$ forbids coherent return from $\mathcal{H}_{\mathrm{RB}}$ to $\mathcal{H}_{\mathrm{reg}}$ on subsequent steps, the reduced regular-sector state $\rho(t + \Delta t) = \operatorname{Tr}_{\mathrm{RB}}\!\left(V_{\Delta t} \rho(t) V_{\Delta t}^\dagger\right)$ satisfies in the $\Delta t \to 0^+$ limit:

$$
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_{k=1}^{m(R_F)} \left(L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\}\right).
\tag{7.2}
$$

In particular, if each excess channel beyond $R_c$ couples with uniform rate $\gamma_0$ via a projection/dephasing operator $Q_k$, defining $\Gamma_F(R_F) := \gamma_0 [R_F - R_c]_+$ yields:
1. **Exact Unitarity Below Threshold ($R_F \le R_c$, $\det\mathsf{G} > 0$):** $m = 0 \implies \Gamma_F = 0$, recovering exact Schrödinger/von Neumann evolution **regardless of particle mass $M$**.
2. **Complete Positivity & Trace Preservation:** For $R_F > R_c$, (7.2) is in exact Gorini–Kossakowski–Sudarshan–Lindblad (GKSL) form, preventing negative probabilities or superluminal signalling.

*Proof.* First check isometry of $V_{\Delta t}$ to $O(\Delta t)$:
$$
V_{\Delta t}^\dagger V_{\Delta t}
= \left(I + \frac{i}{\hbar}H\Delta t - \frac{\Delta t}{2}\sum_k L_k^\dagger L_k\right)\!\left(I - \frac{i}{\hbar}H\Delta t - \frac{\Delta t}{2}\sum_k L_k^\dagger L_k\right) + \Delta t \sum_k L_k^\dagger L_k + O(\Delta t^2) = I + O(\Delta t^2).
$$
Tracing over the orthogonal Roadblock sink basis $\{|r_k\rangle\}_{k=1}^m$ (which cannot interfere back into $\mathcal{H}_{\mathrm{reg}}$ on future steps because $\mathcal{N}_1(|r_k\rangle) = \varnothing$) gives the Kraus map $\rho(t+\Delta t) = K_0 \rho K_0^\dagger + \sum_{k=1}^m K_k \rho K_k^\dagger$ with $K_0 = I - \frac{i}{\hbar}H\Delta t - \frac{\Delta t}{2}\sum_k L_k^\dagger L_k$ and $K_k = \sqrt{\Delta t}\,L_k$. Expanding $\frac{\rho(t+\Delta t) - \rho(t)}{\Delta t}$ and taking $\Delta t \to 0^+$ yields (7.2). When $R_F \le R_c$, $m = 0$, the sum is empty, and $\Gamma_F = 0$ identically. $\blacksquare$

---

### 7.2 Gravitational Freedom-Defect Tensor $\mathcal{K}_{\mu\nu}[\mathsf{G}]$

To couple Freedom Geometry $\mathsf{G}_{AB}(x)$ consistently to emergent spacetime geometry $g_{\mu\nu}(x)$, any candidate $\mathcal{K}_{\mu\nu}$ **must** respect the contracted Bianchi identity $\nabla^\mu G_{\mu\nu} = 0$ (covariant conservation) and local gauge invariance (Theorem 3.2). Ad-hoc tensors violate $\nabla^\mu G_{\mu\nu} = 0$. Instead, we derive $\mathcal{K}_{\mu\nu}$ from the unique lowest-order invariant geometric action on the space of Hermitian positive-definite Freedom metrics $\mathsf{G}(x) \in \mathrm{Herm}_+(k)$.

### Definition 7.2 (Riemannian Geometry on Continuation-Metric Space)
On the manifold $\mathrm{Herm}_+(k)$ of non-singular $k \times k$ Hermitian Freedom metrics $\mathsf{G}$, the unique $GL(k,\mathbb{C})$-congruence-invariant affine-symmetric metric (up to trace coupling $\eta \in \mathbb{R}$) is

$$
ds_{\mathrm{Herm}_+}^2 = \operatorname{Tr}\!\left(\mathsf{G}^{-1} d\mathsf{G}\, \mathsf{G}^{-1} d\mathsf{G}\right) + \eta \left(\operatorname{Tr}(\mathsf{G}^{-1} d\mathsf{G})\right)^2.
\tag{7.3}
$$

Note that $\operatorname{Tr}(\mathsf{G}^{-1}\partial_\mu\mathsf{G}) = \partial_\mu \ln\det\mathsf{G} = 2\,\partial_\mu \ln\mathcal{V}_F$ directly measures gradients of the **CFR Freedom Volume** $\mathcal{V}_F = \sqrt{\det\mathsf{G}}$!

Coupling $\mathsf{G}(x)$ to $(M, g_{\mu\nu})$ with stiffness $\lambda_F$ and optional non-minimal Freedom-curvature coupling $\xi_F$ gives the total effective gravitational action:

$$
S_{\mathrm{grav}}[g, \mathsf{G}, \Psi_{\mathrm{mat}}]
= \int d^4x \sqrt{-g} \left[
\frac{c^3}{16\pi G}\Big((1 + \xi_F \phi_F) R - 2\Lambda\Big)
- \frac{\lambda_F c^3}{32\pi G}\, g^{\mu\nu} \mathcal{M}_{\mu\nu}[\mathsf{G}]
\right] + S_{\mathrm{mat}},
\tag{7.4}
$$

where $\phi_F(x) := \ln\big(\mathcal{V}_F(x)/\mathcal{V}_{F,0}\big)$ and

$$
\mathcal{M}_{\mu\nu}[\mathsf{G}] := \operatorname{Tr}\!\left(\mathsf{G}^{-1}\partial_\mu\mathsf{G}\,\mathsf{G}^{-1}\partial_\nu\mathsf{G}\right) + 4\eta\,(\partial_\mu\phi_F)(\partial_\nu\phi_F).
\tag{7.5}
$$

### Theorem 7.3 (Derived Form and Roadblock Singularity of $\mathcal{K}_{\mu\nu}$)
Varying (7.4) with respect to $g^{\mu\nu}$ yields the CFR-modified Einstein field equation

$$
G_{\mu\nu} + \Lambda_{\mathrm{eff}} g_{\mu\nu} = \frac{8\pi G_{\mathrm{eff}}(x)}{c^4}\, T_{\mu\nu} + \tilde{\mathcal{K}}_{\mu\nu}[\mathsf{G}],
\tag{7.6}
$$

with effective gravitational coupling $G_{\mathrm{eff}}(x) = \frac{G}{1 + \xi_F \phi_F(x)}$ and explicit **CFR Freedom-Defect Tensor** (for minimal coupling $\xi_F = 0$, writing $\tilde{\mathcal{K}}_{\mu\nu} = \frac{\lambda_F}{2}\mathcal{K}_{\mu\nu}$, or in general including the $\xi_F$ improvement term):

$$
\mathcal{K}_{\mu\nu}[\mathsf{G}] = \mathcal{M}_{\mu\nu}[\mathsf{G}] - \frac{1}{2} g_{\mu\nu} g^{\alpha\beta} \mathcal{M}_{\alpha\beta}[\mathsf{G}] + \frac{2\xi_F}{\lambda_F}\left(\nabla_\mu \nabla_\nu \phi_F - g_{\mu\nu} \Box \phi_F\right).
\tag{7.7}
$$

This derived tensor satisfies four structural properties:
1. **Exact Recovery of General Relativity on Uniform Regular Strata:** Whenever $\mathsf{G}(x)$ is constant ($\partial_\mu \mathsf{G} = 0$, $\phi_F = 0$), $\mathcal{K}_{\mu\nu}[\mathsf{G}] = 0$ identically and $G_{\mathrm{eff}} = G$.
2. **Exact Local Gauge Invariance:** Because $\mathsf{G}(x)$ is invariant under all local action rephasings (Theorem 3.2), $\mathcal{K}_{\mu\nu}[\mathsf{G}]$ is strictly gauge-invariant.
3. **Bianchi Consistency ($\nabla^\mu \mathcal{K}_{\mu\nu} = 0$ on-shell):** When $\mathsf{G}(x)$ satisfies its Euler–Lagrange equation from (7.4) — for $\xi_F = \eta = 0$, the harmonic matrix equation $\nabla^\mu(\mathsf{G}^{-1}\nabla_\mu \mathsf{G}) = 0$ — the covariant divergence $\nabla^\mu \mathcal{K}_{\mu\nu} = 0$ vanishes identically.
4. **Roadblock Amplification as $\det\mathsf{G} \to 0$:** Let $\{\lambda_1(x), \dots, \lambda_k(x)\}$ be the positive eigenvalues of $\mathsf{G}(x)$ approaching a soft Roadblock hypersurface $\Sigma_{\mathrm{RB}}$ where $\lambda_1(x) \to 0^+$ with non-zero normal gradient $\partial_n \lambda_1 \neq 0$. Then
   $$
   \mathcal{M}_{nn}[\mathsf{G}] \ge (1 + \eta)\left(\frac{\partial_n \lambda_1}{\lambda_1}\right)^2 \;\underset{\lambda_1 \to 0^+}{\longrightarrow}\; +\infty \qquad (\text{for } 1 + \eta > 0),
   \tag{7.8}
   $$
   and when $\xi_F \neq 0$, the second-derivative term $\nabla_\mu \nabla_\nu \ln\mathcal{V}_F$ can attain **either sign**, modifying local geodesic convergence $R_{\mu\nu} u^\mu u^\nu$ (the Raychaudhuri focusing scalar) without requiring exotic negative-mass matter!

*Proof.*
- Using $\delta\sqrt{-g} = -\frac{1}{2}\sqrt{-g}\, g_{\mu\nu}\delta g^{\mu\nu}$ and the standard Palatini/integration-by-parts variation $\delta\!\int \sqrt{-g}\, f(x) R = \int \sqrt{-g}\left(f G_{\mu\nu} - \nabla_\mu\nabla_\nu f + g_{\mu\nu}\Box f\right)\delta g^{\mu\nu}$, varying (7.4) with respect to $g^{\mu\nu}$ yields:
  $$
  (1 + \xi_F\phi_F) G_{\mu\nu} + \Lambda g_{\mu\nu} - \xi_F(\nabla_\mu\nabla_\nu\phi_F - g_{\mu\nu}\Box\phi_F)
  - \frac{\lambda_F}{2}\left(\mathcal{M}_{\mu\nu} - \frac{1}{2}g_{\mu\nu}g^{\alpha\beta}\mathcal{M}_{\alpha\beta}\right)
  = \frac{8\pi G}{c^4} T_{\mu\nu},
  $$
  which rearranges immediately to (7.6)–(7.7).
- Property (1) and (2) are immediate by inspection.
- For Property (3) ($\xi_F = \eta = 0$), let $J_\mu := \mathsf{G}^{-1}\nabla_\mu\mathsf{G}$. Note the Maurer–Cartan identity $\nabla_\mu J_\nu - \nabla_\nu J_\mu = -\mathsf{G}^{-1}(\nabla_\mu\mathsf{G})\mathsf{G}^{-1}(\nabla_\nu\mathsf{G}) + \mathsf{G}^{-1}(\nabla_\nu\mathsf{G})\mathsf{G}^{-1}(\nabla_\mu\mathsf{G}) = -[J_\mu, J_\nu]$. Differentiating $\mathcal{K}_{\mu\nu} = \operatorname{Tr}(J_\mu J_\nu) - \frac{1}{2}g_{\mu\nu}\operatorname{Tr}(J^\alpha J_\alpha)$:
  $$
  \nabla^\mu \mathcal{K}_{\mu\nu}
  = \operatorname{Tr}\!\left((\nabla^\mu J_\mu) J_\nu + J^\mu \nabla_\mu J_\nu - J^\mu \nabla_\nu J_\mu\right)
  = \operatorname{Tr}\!\left((\nabla^\mu J_\mu) J_\nu + J^\mu (\nabla_\mu J_\nu - \nabla_\nu J_\mu)\right).
  $$
  By the Maurer–Cartan identity, $\operatorname{Tr}(J^\mu [J_\mu, J_\nu]) = \operatorname{Tr}(J^\mu J_\mu J_\nu - J^\mu J_\nu J_\mu) = 0$ by cyclicity of trace! Hence $\nabla^\mu \mathcal{K}_{\mu\nu} = \operatorname{Tr}\big((\nabla^\mu J_\mu) J_\nu\big) = 0$ whenever $\nabla^\mu J_\mu = 0$.
- For Property (4), diagonalize $\mathsf{G}(x) = U(x)\,\mathrm{diag}(\lambda_1,\dots,\lambda_k)\,U(x)^\dagger$ with $U \in U(k)$. Writing $\Omega_n := U^\dagger \partial_n U$ (skew-Hermitian), $\mathsf{G}^{-1}\partial_n\mathsf{G} = U\left(\Lambda_D^{-1}\partial_n\Lambda_D + \Lambda_D^{-1}[\Lambda_D, \Omega_n]\right)U^\dagger$, whose diagonal and off-diagonal blocks are trace-orthogonal:
  $$
  \operatorname{Tr}\!\left((\mathsf{G}^{-1}\partial_n\mathsf{G})^2\right)
  = \sum_{a=1}^k \left(\frac{\partial_n \lambda_a}{\lambda_a}\right)^2 + \sum_{a \neq b} \frac{(\lambda_a - \lambda_b)^2}{\lambda_a \lambda_b} |\Omega_{n,ab}|^2 \ge \left(\frac{\partial_n \lambda_1}{\lambda_1}\right)^2,
  $$
  while $4\eta(\partial_n\phi_F)^2 = \eta\left(\sum_a \frac{\partial_n\lambda_a}{\lambda_a}\right)^2 \sim \eta\left(\frac{\partial_n\lambda_1}{\lambda_1}\right)^2$ as $\lambda_1 \to 0^+$ with $\lambda_{a\ge 2}$ bounded away from $0$, proving (7.8). $\blacksquare$

---

## 8. Quantitative Falsifiable Experimental Protocol

A physical theory is corroborated experimentally only by risking falsification on a quantitative observable where standard theories make a different prediction.

### 8.1 The Experimental Discriminator: Branching Rank $R_F$ vs. Mass $M$
Consider three competing classes of physics in interferometry:
1. **Standard Quantum Mechanics (QM):** Intrinsic decoherence $\Gamma_{\mathrm{int}} = 0$ for all masses $M$ and all coherent continuation ranks $R_F$ once environmental gas/blackbody/vibrational noise $\Gamma_{\mathrm{env}}$ is subtracted.
2. **Gravitational / Mass-Proportional Collapse (Diósi–Penrose, CSL):** Intrinsic decoherence scales quadratically with particle/nucleon mass, $\Gamma_{\mathrm{CSL}}(M, R_F) \propto (M / m_0)^2$, and is **independent of multi-port path rank $R_F$** at fixed spatial delocalization $\Delta x$ — and vanishes ($M = 0$) for single photons!
3. **CFR Roadblock Decoherence (Theorem 7.1):** Intrinsic decoherence depends on the **effective Freedom rank** $R_F = \operatorname{rank}\mathsf{G}^{(L)}(h)$ of simultaneously open, mutually orthogonal coherent continuation channels:
   $$
   \Gamma_{\mathrm{CFR}}(M, R_F) = \gamma_* \left[\frac{R_F - R_c}{R_c}\right]_+^p,
   \tag{8.1}
   $$
   which is **zero for arbitrarily large macromolecules ($M \gg 10^4\text{ amu}$) in 2-path Talbot–Lau interferometers ($R_F = 2 < R_c$)** — consistent with Arndt/Fein macromolecule interference experiments — yet predicts a **sharp non-analytic visibility kink** as $R_F$ is swept past $R_c$ even for **massless photons ($M = 0$)** or light ultracold atoms!

### 8.2 Concrete Experimental Protocol: Programmable $N$-Port Multi-Path Interferometry
Construct a programmable integrated-photonic or optical-lattice $N$-path interferometer ($N$ tunable from $2$ up to $N_{\max}$) preparing the balanced continuation state
$$
|\psi_N\rangle = \frac{1}{\sqrt{N}} \sum_{A=1}^N e^{i\phi_A} |\text{path } A\rangle
$$
held for coherent dwell time $\tau_{\mathrm{dwell}}$, where an active subset of $R_F \le N$ paths are open ($\mathcal{N}_1$ controlled via programmable Mach–Zehnder attenuators/shutters while keeping total optical path length $L_{\mathrm{opt}}$ and thermal load constant via dummy compensation heaters).

Measure normalized interference fringe visibility $V(R_F, \tau_{\mathrm{dwell}})$ at the recombination port:

$$
\ln \frac{V(R_F, \tau_{\mathrm{dwell}})}{V_{\mathrm{cal}}(R_F, 0)} = -\Big(\Gamma_{\mathrm{env}}(R_F) + \Gamma_{\mathrm{CFR}}(R_F)\Big)\,\tau_{\mathrm{dwell}}.
\tag{8.2}
$$

### 8.3 Three Clean Differential Control Signatures
To eliminate ordinary technical phase noise ($\Gamma_{\mathrm{env}}$ scaling smoothly with port count $N$):
1. **Non-analytic kink test ($\Delta^2_R \ln V$):** Environmental dephasing per path adds smoothly ($\Gamma_{\mathrm{env}}(R_F) = \gamma_1 + \gamma_2 R_F$, smooth in $R_F$), whereas CFR predicts $\Gamma_{\mathrm{CFR}}(R_F) \equiv 0$ for all $R_F \le R_c$ followed by a sudden onset at $R_F > R_c$.
2. **Soft-Roadblock Pinching Control (Theorem 3.4 Test):** Keep all $N > R_c$ physical wave-guides open (identical hardware, identical $\Gamma_{\mathrm{env}}$!), but continuously tune downstream couplers so pairs of paths merge into collinear future continuations, reducing $\operatorname{rank}\mathsf{G}^{(L)}$ from $N$ below $R_c$ without closing physical shutters.
   - *Technical noise prediction:* Unchanged ($\Gamma_{\mathrm{env}}$ depends on physical hardware channels $N$).
   - *CFR prediction:* $\Gamma_{\mathrm{CFR}}$ **switches off** as soon as $\operatorname{rank}\mathsf{G}^{(L)} \le R_c$!
3. **Mass-Independence Cross-Check:** Run the same rank sweep $R_F \in [2, N_{\max}]$ on (a) single photons ($M = 0$) and (b) Bose–Einstein / matter-wave lattice splitters ($M > 0$). Matching $R_c$ across $M = 0$ and $M > 0$ falsifies CSL/DP; null kink up to $N_{\max}$ places a rigorous experimental lower bound $R_c > N_{\max}$ (or upper bound on $\gamma_*$).
