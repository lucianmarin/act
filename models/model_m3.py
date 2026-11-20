# models/model_m3.py
"""
M3: Emergent Causal Structure, Kinematic Roadblock `c`, and Lorentzian Signature

Implements Theorem 2.7 and Section 5 of cfr/cfr-proofs.md (pure Python):
  - Local 1D lattice action propagation proving exact Kinematic Roadblock
    outside the causal cone |x - x_0| <= L (c_max = 1 hop/step)
  - Causal action diamond identity: 4 N_+ N_- = T^2 - X^2 / c^2
  - Uniqueness and boost invariance of proper-tick functional tau = 2 sqrt(N_+ N_-)
  - Extraction of the (1+3)D metric tensor g_mu_nu from -c^2 d(tau)^2 and
    verification of Lorentzian signature (-, +, +, +).
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

try:
    from models.model_m1 import Action, FiniteActionModel, intervention_effect
except ImportError:
    from model_m1 import Action, FiniteActionModel, intervention_effect


def build_causal_cone_lattice(radius: int = 4, max_steps: int = 3, c_hops: int = 1) -> FiniteActionModel:
    """
    Build a (1+1)D layered action network of emergent configurations (t, x)
    with x in [-radius, radius], t in [0, max_steps], where each elementary step
    can change x by dx in [-c_hops, +c_hops] (nearest-neighbor locality).
    """
    actions: List[Action] = []
    norm = 1.0 / math.sqrt(2 * c_hops + 1)
    for t in range(max_steps):
        for x in range(-radius, radius + 1):
            for dx in range(-c_hops, c_hops + 1):
                nx = x + dx
                if -radius <= nx <= radius:
                    src = f"t{t}_x{x}"
                    dst = f"t{t+1}_x{nx}"
                    actions.append(Action(f"{src}->{dst}", src, dst, norm + 0.0j))
    return FiniteActionModel(actions)


def verify_kinematic_roadblock_cone(max_steps: int = 3) -> Dict[str, object]:
    """
    Verify Theorem 2.7:
      1. Starting at (t=0, x=0), transition amplitude to (t=L, x) is strictly 0
         outside |x| <= L (Kinematic Roadblock).
      2. Disabling an action at (t=1, x_pert=2) has zero effect on probabilities
         at (t=2, x_target=-1) because |x_target - x_pert| = 3 > remaining steps (1).
    """
    radius = max_steps + 2
    lattice = build_causal_cone_lattice(radius=radius, max_steps=max_steps, c_hops=1)

    outside_amplitudes: List[float] = []
    inside_amplitudes: List[float] = []
    for x in range(-radius, radius + 1):
        amp = abs(lattice.transition_amplitude("t0_x0", f"t{max_steps}_x{x}", exact_depth=max_steps))
        if abs(x) > max_steps:
            outside_amplitudes.append(amp)
        else:
            inside_amplitudes.append(amp)

    # Local intervention at t=1, x=+2 cannot affect t=2, x=-1 (distance 3 > Δt=1)
    spacelike_check = intervention_effect(
        lattice,
        src="t0_x0",
        dst="t2_x-1",
        intervention_disabled={"t1_x2->t2_x1", "t1_x2->t2_x2", "t1_x2->t2_x3"},
        max_depth=2,
    )
    # Timelike/null intervention at t=1, x=0 DOES affect t=2, x=0 (distance 0 <= Δt=1)
    timelike_check = intervention_effect(
        lattice,
        src="t0_x0",
        dst="t2_x0",
        intervention_disabled={"t1_x0->t2_x0"},
        max_depth=2,
    )
    return {
        "max_outside_cone_amp": max(outside_amplitudes) if outside_amplitudes else 0.0,
        "max_inside_cone_amp": max(inside_amplitudes) if inside_amplitudes else 0.0,
        "spacelike_no_signalling": not bool(spacelike_check["effect"]),
        "timelike_influence_present": bool(timelike_check["effect"]),
    }


class CausalDiamondMetric:
    """
    Implements Theorem 5.2: emergent Lorentzian proper-tick interval from CFR
    directional action counts (N_+, N_-).
    """

    def __init__(self, c: float = 1.0) -> None:
        if c <= 0:
            raise ValueError("Propagation bound c must be positive.")
        self.c = c

    def proper_ticks_from_counts(self, n_plus: float, n_minus: float) -> float:
        """tau(N_+, N_-) = 2 * sqrt(N_+ * N_-) (Equation 5.2)."""
        if n_plus < 0 or n_minus < 0:
            raise ValueError("Outside admissible future cone (Kinematic Roadblock).")
        return 2.0 * math.sqrt(n_plus * n_minus)

    def coords_from_counts(self, n_plus: float, n_minus: float) -> Tuple[float, float]:
        """T = N_+ + N_-, X = c * (N_+ - N_-)."""
        return (n_plus + n_minus, self.c * (n_plus - n_minus))

    def boost_counts(self, n_plus: float, n_minus: float, rapidity: float) -> Tuple[float, float]:
        """Cone-preserving automorphism (N_+, N_-) -> (e^eta N_+, e^-eta N_-)."""
        return (math.exp(rapidity) * n_plus, math.exp(-rapidity) * n_minus)

    def interval_squared_3plus1(self, dt: float, dx: Sequence[float]) -> float:
        """ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2 (Equation 5.3)."""
        if len(dx) != 3:
            raise ValueError("Expected 3 spatial displacement components.")
        return -(self.c ** 2) * (dt ** 2) + sum(comp ** 2 for comp in dx)

    def extract_metric_tensor_hessian(self, eps: float = 1e-5) -> List[List[float]]:
        """
        Numerically extract g_{mu nu} = (1/2) d^2(ds^2) / (dx^mu dx^nu) from the
        CFR proper-tick functional in (t, x, y, z) coordinates inside the causal cone.
        """
        def ds2(coords: List[float]) -> float:
            dt, x, y, z = coords
            r = math.sqrt(x * x + y * y + z * z)
            n_plus = 0.5 * (dt + r / self.c)
            n_minus = 0.5 * (dt - r / self.c)
            tau = self.proper_ticks_from_counts(n_plus, n_minus)
            return -(self.c ** 2) * (tau ** 2)

        # Evaluate around a strictly timelike displacement so N_+ > 0, N_- > 0
        base = [2.0, 0.2, -0.15, 0.1]
        g = [[0.0 for _ in range(4)] for _ in range(4)]
        for mu in range(4):
            for nu in range(4):
                pp = base[:]
                pm = base[:]
                mp = base[:]
                mm = base[:]
                pp[mu] += eps
                pp[nu] += eps
                pm[mu] += eps
                pm[nu] -= eps
                mp[mu] -= eps
                mp[nu] += eps
                mm[mu] -= eps
                mm[nu] -= eps
                d2 = (ds2(pp) - ds2(pm) - ds2(mp) + ds2(mm)) / (4.0 * eps * eps)
                g[mu][nu] = 0.5 * d2
        return g

    @staticmethod
    def signature_counts(metric_diag_approx: List[List[float]], tol: float = 1e-6) -> Tuple[int, int]:
        """
        Count (n_negative, n_positive) eigenvalues of a symmetric 4x4 matrix via
        classical Jacobi diagonalization (pure Python, zero dependencies).
        """
        n = len(metric_diag_approx)
        a = [row[:] for row in metric_diag_approx]
        for _ in range(60):
            # Find largest off-diagonal entry
            p, q = 0, 1
            max_off = 0.0
            for i in range(n):
                for j in range(i + 1, n):
                    if abs(a[i][j]) > max_off:
                        max_off = abs(a[i][j])
                        p, q = i, j
            if max_off <= 1e-14:
                break
            if abs(a[p][p] - a[q][q]) <= 1e-15:
                phi = math.pi / 4.0
            else:
                phi = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
            c_phi = math.cos(phi)
            s_phi = math.sin(phi)
            app = c_phi * c_phi * a[p][p] - 2.0 * s_phi * c_phi * a[p][q] + s_phi * s_phi * a[q][q]
            aqq = s_phi * s_phi * a[p][p] + 2.0 * s_phi * c_phi * a[p][q] + c_phi * c_phi * a[q][q]
            a[p][p] = app
            a[q][q] = aqq
            a[p][q] = 0.0
            a[q][p] = 0.0
            for k in range(n):
                if k != p and k != q:
                    akp = c_phi * a[k][p] - s_phi * a[k][q]
                    akq = s_phi * a[k][p] + c_phi * a[k][q]
                    a[k][p] = a[p][k] = akp
                    a[k][q] = a[q][k] = akq

        eigs = [a[i][i] for i in range(n)]
        neg = sum(1 for e in eigs if e < -tol)
        pos = sum(1 for e in eigs if e > tol)
        return (neg, pos)


def demo() -> None:
    print("=== Model M3: Emergent Causal Cones & Lorentzian Signature ===")
    cone = verify_kinematic_roadblock_cone(max_steps=3)
    print(f"Max amplitude outside causal cone:    {cone['max_outside_cone_amp']:.2e}")
    print(f"Spacelike intervention no-signalling: {cone['spacelike_no_signalling']}")
    print(f"Timelike intervention active:         {cone['timelike_influence_present']}")

    geom = CausalDiamondMetric(c=1.0)
    tau_0 = geom.proper_ticks_from_counts(9.0, 4.0)
    bp, bm = geom.boost_counts(9.0, 4.0, rapidity=0.85)
    tau_boosted = geom.proper_ticks_from_counts(bp, bm)
    t_coord, x_coord = geom.coords_from_counts(9.0, 4.0)
    print(f"Proper ticks 2*sqrt(N+N-):            {tau_0:.6f}")
    print(f"Boosted proper ticks (eta=0.85):      {tau_boosted:.6f}")
    print(f"sqrt(T^2 - X^2/c^2):                  {math.sqrt(t_coord**2 - x_coord**2):.6f}")

    g_mat = geom.extract_metric_tensor_hessian()
    neg, pos = geom.signature_counts(g_mat)
    print(f"Extracted 4D metric signature:        ({neg} negative, {pos} positive) => (-,+,+,+)")


if __name__ == "__main__":
    demo()
