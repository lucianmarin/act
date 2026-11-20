# models/model_m2.py
"""
M2: Canonical Freedom Geometry G_AB(h), Freedom Volume V_F, and Roadblocks

Implements Section 3 of cfr/cfr-proofs.md using pure Python (no external deps):
  - Microscopic horizon-L continuation vectors Psi_A^(L)(x | h) (Definition 3.1)
  - Hermitian Gram metric G_AB^(L)(h) = <Psi_A^(L) | Psi_B^(L)>
  - Exact U(1) local gauge invariance of G_AB^(L)(h) and V_F (Theorem 3.2)
  - Roadblock Rank Theorem (Theorem 3.4): unifies Hard Roadblocks (N_1 = empty),
    Interference Roadblocks (Psi_A == 0), and Collinear/Merging Roadblocks
    (rank G < |N_1|)
  - Smooth Fubini-Study metric limit G_ab^FS (Proposition 3.5)
"""

from __future__ import annotations

import cmath
import math
from typing import Callable, Dict, List, Sequence, Tuple

try:
    from models.model_m1 import Action, FiniteActionModel, gauge_transform, matrix_rank
except ImportError:
    from model_m1 import Action, FiniteActionModel, gauge_transform, matrix_rank


def complex_det(mat: List[List[complex]], tol: float = 1e-12) -> complex:
    """Compute determinant of a square complex matrix via Gaussian elimination with partial pivoting."""
    n = len(mat)
    if n == 0:
        return 0.0 + 0.0j
    m = [row[:] for row in mat]
    sign = 1.0
    det = 1.0 + 0.0j

    for col in range(n):
        pivot = col
        best = abs(m[col][col])
        for r in range(col + 1, n):
            if abs(m[r][col]) > best:
                best = abs(m[r][col])
                pivot = r
        if best <= tol:
            return 0.0 + 0.0j
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            sign = -sign
        piv_val = m[col][col]
        det *= piv_val
        for r in range(col + 1, n):
            factor = m[r][col] / piv_val
            for c in range(col, n):
                m[r][c] -= factor * m[col][c]

    return sign * det


def max_matrix_diff(a: List[List[complex]], b: List[List[complex]]) -> float:
    """Maximum entrywise modulus difference between two equal-shaped matrices."""
    if not a and not b:
        return 0.0
    return max(
        abs(a[i][j] - b[i][j])
        for i in range(len(a))
        for j in range(len(a[0]))
    )


class FreedomGeometry:
    """
    Canonical CFR Freedom Geometry G_AB^(L)(h) at a node/state [h] for horizon L >= 1.
    """

    def __init__(
        self,
        model: FiniteActionModel,
        node: str,
        horizon: int = 2,
        tol: float = 1e-10,
    ) -> None:
        if horizon < 1:
            raise ValueError("Horizon L must be >= 1.")
        self.model = model
        self.node = node
        self.horizon = horizon
        self.tol = tol
        self.initial_actions: List[Action] = model.outgoing(node)
        self.target_nodes: List[str] = model.nodes()
        self.continuation_vectors: List[List[complex]] = self._compute_continuation_vectors()
        self.G: List[List[complex]] = self._compute_gram_metric()

    def _compute_continuation_vectors(self) -> List[List[complex]]:
        """
        Compute Psi_A^(L)(x | h) for each initial admissible branch alpha_A in N_1(h)
        and each state x in S_CFR (Equation 3.1).
        """
        node_idx = {x: i for i, x in enumerate(self.target_nodes)}
        vectors: List[List[complex]] = []

        for alpha in self.initial_actions:
            vec = [0.0 + 0.0j] * len(self.target_nodes)
            if self.horizon == 1:
                if self.model.path_allowed((alpha.name,)):
                    vec[node_idx[alpha.dst]] += alpha.weight
            else:
                for tail in self.model.iter_paths(
                    start=alpha.dst,
                    end=None,
                    exact_depth=self.horizon - 1,
                ):
                    full_path = (alpha.name,) + tail
                    if not self.model.path_allowed(full_path):
                        continue
                    end_node = self.model.endpoint_after_path(self.node, full_path)
                    if end_node is not None:
                        vec[node_idx[end_node]] += self.model.path_weight(full_path)
            vectors.append(vec)

        return vectors

    def _compute_gram_metric(self) -> List[List[complex]]:
        """G_AB^(L)(h) = sum_x conj(Psi_A^(L)(x|h)) * Psi_B^(L)(x|h) (Equation 3.2)."""
        k = len(self.continuation_vectors)
        g = [[0.0 + 0.0j for _ in range(k)] for _ in range(k)]
        for a in range(k):
            va = self.continuation_vectors[a]
            for b in range(k):
                vb = self.continuation_vectors[b]
                g[a][b] = sum(va[x].conjugate() * vb[x] for x in range(len(va)))
        return g

    def det(self) -> float:
        """Determinant of G_AB^(L)(h) (real and >= 0 for positive semi-definite Gram matrix)."""
        if not self.initial_actions:
            return 0.0
        d = complex_det(self.G, tol=self.tol).real
        return max(0.0, d)

    def freedom_volume(self) -> float:
        """V_F^(L)(h) = sqrt(det G^(L)(h)), or 0 when N_1(h) is empty (Equation 3.3)."""
        if not self.initial_actions:
            return 0.0
        return math.sqrt(self.det())

    def rank(self) -> int:
        """Effective Freedom dimension F_eff^(L)(h) = rank G^(L)(h)."""
        return matrix_rank(self.G, tol=self.tol)

    def classify_regime(self) -> str:
        """
        Classify node into Regular vs the three Roadblock mechanisms of Theorem 3.4:
          - 'hard_roadblock'         : N_1(h) == empty
          - 'interference_roadblock' : some branch has Psi_A^(L) == 0 identically
          - 'collinear_roadblock'    : all Psi_A^(L) != 0, but rank G < |N_1(h)|
          - 'regular'                : V_F > 0 (full rank |N_1(h)|)
        """
        k = len(self.initial_actions)
        if k == 0:
            return "hard_roadblock"
        for vec in self.continuation_vectors:
            norm_sq = sum(abs(z) ** 2 for z in vec)
            if norm_sq <= self.tol ** 2:
                return "interference_roadblock"
        if self.rank() < k or self.freedom_volume() <= self.tol:
            return "collinear_roadblock"
        return "regular"


def fubini_study_metric(
    state_fn: Callable[[Sequence[float]], List[complex]],
    theta: Sequence[float],
    eps: float = 1e-6,
) -> List[List[float]]:
    """
    Evaluate the smooth Fubini-Study continuation metric G_ab^FS(theta) (Prop. 3.5):
        G_ab^FS = Re[ <d_a psi | d_b psi> - <psi | d_a psi><d_b psi | psi> ].
    """
    def normalize(v: List[complex]) -> List[complex]:
        nrm = math.sqrt(sum(abs(z) ** 2 for z in v))
        if nrm == 0.0:
            raise ValueError("Continuation state vanished.")
        return [z / nrm for z in v]

    psi = normalize(state_fn(theta))
    m = len(theta)
    d_psi: List[List[complex]] = []
    for a in range(m):
        tp = list(theta)
        tm = list(theta)
        tp[a] += eps
        tm[a] -= eps
        vp = normalize(state_fn(tp))
        vm = normalize(state_fn(tm))
        d_psi.append([(vp[i] - vm[i]) / (2.0 * eps) for i in range(len(psi))])

    g_fs = [[0.0 for _ in range(m)] for _ in range(m)]
    for a in range(m):
        psi_da = sum(psi[i].conjugate() * d_psi[a][i] for i in range(len(psi)))
        for b in range(m):
            da_db = sum(d_psi[a][i].conjugate() * d_psi[b][i] for i in range(len(psi)))
            db_psi = sum(d_psi[b][i].conjugate() * psi[i] for i in range(len(psi)))
            g_fs[a][b] = (da_db - psi_da * db_psi).real
    return g_fs


def build_roadblock_zoo(phase_interference: float = math.pi) -> Dict[str, FreedomGeometry]:
    """
    Construct four canonical CFR graphs illustrating Regular evolution alongside
    all three Roadblock mechanisms proved in Theorem 3.4.
    """
    # 1. Regular 2-branch orthogonal continuations (V_F > 0, rank = 2)
    m_reg = FiniteActionModel(
        [
            Action("h->a", "h", "a", 1.0 + 0j),
            Action("h->b", "h", "b", 1.0 + 0j),
            Action("a->x1", "a", "x1", 1.0 + 0j),
            Action("b->x2", "b", "x2", 1.0 + 0j),
        ]
    )
    # 2. Hard Roadblock: N_1(h) == empty
    m_hard = m_reg.with_disabled({"h->a", "h->b"})
    # 3. Interference Roadblock: branch h->a splits into two subpaths to x1 with phase pi
    m_interf = FiniteActionModel(
        [
            Action("h->a", "h", "a", 1.0 + 0j),
            Action("h->b", "h", "b", 1.0 + 0j),
            Action("a->x1_u", "a", "x1", 0.5 + 0j),
            Action("a->x1_d", "a", "x1", 0.5 * cmath.exp(1j * phase_interference)),
            Action("b->x2", "b", "x2", 1.0 + 0j),
        ]
    )
    # 4. Collinear / Merging Roadblock: distinct initial branches h->a, h->b land on
    # proportional continuation vectors at horizon L=2
    m_collinear = FiniteActionModel(
        [
            Action("h->a", "h", "a", 1.0 + 0j),
            Action("h->b", "h", "b", 1.0 + 0j),
            Action("a->x1", "a", "x1", 1.0 + 0j),
            Action("b->x1", "b", "x1", cmath.exp(0.7j)),
        ]
    )
    return {
        "regular": FreedomGeometry(m_reg, "h", horizon=2),
        "hard": FreedomGeometry(m_hard, "h", horizon=2),
        "interference": FreedomGeometry(m_interf, "h", horizon=2),
        "collinear": FreedomGeometry(m_collinear, "h", horizon=2),
    }


def demo() -> None:
    print("=== Model M2: Canonical Freedom Geometry & Roadblock Rank Theorem ===")
    zoo = build_roadblock_zoo()
    for label, fg in zoo.items():
        print(
            f"{label:13s}: |N_1|={len(fg.initial_actions)}  rank={fg.rank()}  "
            f"V_F={fg.freedom_volume():.6f}  regime={fg.classify_regime()}"
        )

    # Verify exact U(1) local gauge invariance (Theorem 3.2)
    phases = {"h": 0.91, "a": -1.43, "b": 2.15, "x1": -0.77, "x2": 1.62}
    fg_orig = zoo["regular"]
    fg_gauged = FreedomGeometry(gauge_transform(fg_orig.model, phases), "h", horizon=2)
    print(f"Max |G' - G| under local U(1) gauge:  {max_matrix_diff(fg_orig.G, fg_gauged.G):.2e}")


if __name__ == "__main__":
    demo()
