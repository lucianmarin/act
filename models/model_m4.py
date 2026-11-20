# models/model_m4.py
"""
M4: Derived Matter, Topological Stiffness (Mass), Noether Energy, and E = mc^2

Implements Corollary 5.3 of cfr/cfr-proofs.md and research/mass-energy-equivalence.md:
  - Matter as a periodic localized CFR action pattern cycling with topological
    stiffness mu across causal diamond steps (N_+, N_-)
  - Derivation of effective Lagrangian L(v) = -mu c^2 (d tau / dt) directly
    from the CFR proper-tick count tau = 2 sqrt(N_+ N_-)
  - Numerical Legendre transform verifying canonical momentum p(v), Noether
    energy E(v), rest equivalence E_0 = m c^2, and dispersion E^2 = p^2 c^2 + m^2 c^4
  - Kinematic Roadblock dissolution (d tau -> 0 as v -> c) and phase-transition
    conservation into massless null-boundary radiation modes (m c^2 = E_+ + E_-).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict

try:
    from models.model_m3 import CausalDiamondMetric
except ImportError:
    from model_m3 import CausalDiamondMetric


@dataclass(frozen=True)
class CFRMatterPattern:
    """
    A persistent localized CFR action knot with invariant internal topological
    stiffness `stiffness_mu` (rate of action per unit proper tick) propagating
    through a causal network with null Roadblock bound `c`.
    """

    stiffness_mu: float
    c: float = 1.0

    def __post_init__(self) -> None:
        if self.stiffness_mu < 0:
            raise ValueError("Topological stiffness mu must be >= 0.")
        if self.c <= 0:
            raise ValueError("Kinematic Roadblock speed c must be > 0.")

    def counts_for_velocity(self, v: float, total_steps: float = 1.0) -> tuple[float, float]:
        """Map emergent velocity v in (-c, c) to directional action counts (N_+, N_-)."""
        if abs(v) > self.c:
            raise ValueError("Velocity exceeds Kinematic Roadblock c (inadmissible).")
        n_plus = 0.5 * total_steps * (1.0 + v / self.c)
        n_minus = 0.5 * total_steps * (1.0 - v / self.c)
        return (n_plus, n_minus)

    def effective_lagrangian(self, v: float) -> float:
        """
        Evaluate L(v) = dS / dt from CFR proper-tick functional tau = 2 sqrt(N_+ N_-):
            S = -mu * c^2 * tau  ==>  L(v) = -mu * c^2 * (tau / T).
        """
        if abs(v) >= self.c:
            return 0.0
        diamond = CausalDiamondMetric(c=self.c)
        n_plus, n_minus = self.counts_for_velocity(v, total_steps=1.0)
        tau_per_unit_t = diamond.proper_ticks_from_counts(n_plus, n_minus)
        return -self.stiffness_mu * (self.c ** 2) * tau_per_unit_t

    def canonical_momentum(self, v: float, eps: float = 1e-6) -> float:
        """Compute canonical momentum p = dL/dv numerically via central finite difference."""
        step = eps * self.c
        if abs(v) + step >= self.c:
            raise ValueError("Too close to Kinematic Roadblock c for massive pattern.")
        return (self.effective_lagrangian(v + step) - self.effective_lagrangian(v - step)) / (
            2.0 * step
        )

    def noether_energy(self, v: float, eps: float = 1e-6) -> float:
        """Legendre transform for time-translation Noether invariant: E = p*v - L."""
        p = self.canonical_momentum(v, eps=eps)
        return p * v - self.effective_lagrangian(v)

    def inertial_mass(self, eps: float = 1e-4) -> float:
        """
        Operational inertial mass m := dp/dv|_{v=0} = d^2 L / dv^2|_{v=0}
        (resistance to redirecting the stationary action pattern). Proves m == stiffness_mu!
        """
        h = eps * self.c
        l_pos = self.effective_lagrangian(h)
        l_zero = self.effective_lagrangian(0.0)
        l_neg = self.effective_lagrangian(-h)
        return (l_pos - 2.0 * l_zero + l_neg) / (h * h)

    def verify_dispersion_and_equivalence(self, v: float) -> Dict[str, float]:
        """Verify E_0 = m c^2 and E(v)^2 - p(v)^2 c^2 == m^2 c^4."""
        m_inertial = self.inertial_mass()
        e0 = self.noether_energy(0.0)
        p = self.canonical_momentum(v)
        e = self.noether_energy(v)
        lhs = e * e - (p * self.c) ** 2
        rhs = (m_inertial * (self.c ** 2)) ** 2
        n_plus, n_minus = self.counts_for_velocity(v, total_steps=1.0)
        proper_tick_ratio = 2.0 * math.sqrt(n_plus * n_minus)
        return {
            "stiffness_mu": self.stiffness_mu,
            "inertial_mass_m": m_inertial,
            "rest_energy_E0": e0,
            "mc2": m_inertial * (self.c ** 2),
            "rest_equivalence_error": abs(e0 - m_inertial * (self.c ** 2)),
            "dispersion_error": abs(lhs - rhs),
            "proper_tick_fraction": proper_tick_ratio,
        }

    def annihilate_to_null_modes(self, v: float = 0.0) -> Dict[str, float]:
        """
        Model Section 4 of research/mass-energy-equivalence.md:
        Dissolution of a massive knot (m > 0, |v| < c) into counter-propagating
        massless boundary radiation modes (m = 0, v = +c and v = -c, where N_- = 0
        or N_+ = 0 on the Kinematic Roadblock) conserving total energy & momentum.
        """
        e_total = self.noether_energy(v)
        p_total = self.canonical_momentum(v)
        # Solve E_+ + E_- = E_total and (E_+ - E_-) / c = p_total
        e_plus = 0.5 * (e_total + p_total * self.c)
        e_minus = 0.5 * (e_total - p_total * self.c)
        return {
            "initial_energy": e_total,
            "initial_momentum": p_total,
            "E_gamma_plus": e_plus,
            "E_gamma_minus": e_minus,
            "energy_conservation_err": abs((e_plus + e_minus) - e_total),
            "momentum_conservation_err": abs(((e_plus - e_minus) / self.c) - p_total),
        }


def demo() -> None:
    print("=== Model M4: Derived Matter, Topological Stiffness, and E = mc^2 ===")
    knot = CFRMatterPattern(stiffness_mu=2.5, c=3.0)
    chk = knot.verify_dispersion_and_equivalence(v=1.8)
    print(f"Topological stiffness mu:             {chk['stiffness_mu']:.6f}")
    print(f"Derived inertial mass m = dp/dv|0:    {chk['inertial_mass_m']:.6f}")
    print(f"Rest energy E_0 vs m*c^2:             {chk['rest_energy_E0']:.6f} vs {chk['mc2']:.6f}")
    print(f"|E^2 - p^2 c^2 - m^2 c^4| at v=0.6c:  {chk['dispersion_error']:.2e}")

    ann = knot.annihilate_to_null_modes(v=1.2)
    print(
        f"Annihilation to null modes (v=±c):    E+={ann['E_gamma_plus']:.4f}, "
        f"E-={ann['E_gamma_minus']:.4f} (err={ann['energy_conservation_err']:.2e})"
    )


if __name__ == "__main__":
    demo()
