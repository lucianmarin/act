# models/predictions.py
"""
CFR Predictions and Falsifiable Multi-Path Interferometry Protocol

Implements Section 7.1 and Section 8 of cfr/cfr-proofs.md (pure Python):
  - Microscopic Kraus / GKSL step evolution tracing over Roadblocked sink
    channels (Theorem 7.1), proving exact unitarity below rank threshold R_c
    (independent of particle mass M) and CPTP decoherence above R_c
  - Quantitative visibility predictions for programmable N-port interferometry
    comparing Standard QM, Mass-Collapse (CSL / Diosi-Penrose), and CFR
    Freedom-Rank Roadblock Decoherence — including the Soft-Roadblock Pinching
    Control test (Section 8.3).
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List

try:
    from models.model_m1 import Action, FiniteActionModel
    from models.model_m2 import FreedomGeometry
except ImportError:
    from model_m1 import Action, FiniteActionModel
    from model_m2 import FreedomGeometry


class CFRPredictions:
    """Quantitative CFR candidate deviations from Standard QM and GR."""

    @staticmethod
    def roadblock_correction(lambda_F: float, K_mu_nu: float) -> float:
        """
        Effective gravitational modification lambda_F * K_mu_nu[G] from Theorem 7.3.
        """
        return lambda_F * K_mu_nu

    @staticmethod
    def threshold_decoherence(
        rank_F: int,
        rank_c: int,
        gamma_star: float,
        power: float = 1.0,
    ) -> float:
        """
        CFR threshold decoherence rate (Equation 8.1):
            Gamma_CFR(R_F) = gamma_star * max(0, (R_F - R_c) / R_c)^p.
        Strictly 0 when rank_F <= rank_c, regardless of particle mass M.
        """
        if rank_c <= 0:
            raise ValueError("Critical rank R_c must be >= 1.")
        if rank_F <= rank_c:
            return 0.0
        return gamma_star * (((rank_F - rank_c) / float(rank_c)) ** power)

    @staticmethod
    def strong_distortion_signature(V_F: float, det_G: float, tol: float = 1e-10) -> bool:
        """True when approaching a CFR Roadblock (det G -> 0 or V_F -> 0)."""
        return abs(det_G) < tol or V_F < tol


def kraus_roadblock_step(
    rho: List[List[complex]],
    rank_F: int,
    rank_c: int,
    gamma_0: float,
    dt: float,
) -> List[List[complex]]:
    """
    Execute one microscopic Kraus step of Theorem 7.1 on an N x N density matrix `rho`
    over N open interferometer paths when `m = max(0, rank_F - rank_c)` Roadblocked
    sink channels absorb phase coherence from the highest excess branches.

    Preserves Tr(rho) == 1 and Hermiticity/positivity identically.
    """
    n = len(rho)
    excess = max(0, min(n, rank_F - rank_c))
    if excess == 0 or gamma_0 == 0.0 or dt == 0.0:
        return [row[:] for row in rho]

    # Each excess channel k in [n - excess, n - 1] couples to a path-dephasing sink L_k = sqrt(gamma_0) |k><k|
    p_leak = min(1.0, gamma_0 * dt)
    survive = math.sqrt(1.0 - p_leak)
    out = [[0.0 + 0j for _ in range(n)] for _ in range(n)]
    leaked_Indices = set(range(n - excess, n))

    for i in range(n):
        si = survive if i in leaked_Indices else 1.0
        for j in range(n):
            sj = survive if j in leaked_Indices else 1.0
            out[i][j] = (si * sj) * rho[i][j]
            if i == j and i in leaked_Indices:
                # Kraus sink trace restores diagonal population (pure dephasing / record creation)
                out[i][i] += p_leak * rho[i][i]
    return out


def fringe_visibility(rho: List[List[complex]]) -> float:
    """
    Normalized multi-path coherence visibility V in [0, 1]:
        V = (1 / (N - 1)) * sum_{i != j} |rho_{ij}| * N / Tr(rho)
    Equals 1.0 for a pure balanced N-path superposition and 0.0 for completely dephased paths.
    """
    n = len(rho)
    if n <= 1:
        return 1.0
    off_sum = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                off_sum += abs(rho[i][j])
    tr = sum(rho[i][i].real for i in range(n))
    return off_sum / ((n - 1) * tr)


def build_n_port_interferometer_graph(n_ports: int, pinched_pairs: int = 0) -> FreedomGeometry:
    """
    Build an N-port interferometer action graph from source 'in' through N arms
    a_0 .. a_{N-1}. If `pinched_pairs > 0`, merge `pinched_pairs` arms onto shared
    downstream states (Soft-Roadblock Pinching Control of Section 8.3: physical
    arm count stays N, while effective Freedom rank drops to N - pinched_pairs!).
    """
    actions: List[Action] = []
    amp = 1.0 / math.sqrt(n_ports)
    for k in range(n_ports):
        actions.append(Action(f"in->arm_{k}", "in", f"arm_{k}", amp + 0j))
        # First `pinched_pairs` arms merge onto arm_{k + pinched_pairs}'s target node
        if k < pinched_pairs and (k + pinched_pairs) < n_ports:
            target = f"out_{k + pinched_pairs}"
        else:
            target = f"out_{k}"
        actions.append(Action(f"arm_{k}->{target}", f"arm_{k}", target, 1.0 + 0j))
    return FreedomGeometry(FiniteActionModel(actions), "in", horizon=2)


def compare_competing_theories(
    n_ports: int,
    mass_amu: float,
    dwell_time: float = 1.0,
    rank_c: int = 4,
    gamma_star: float = 0.8,
    gamma_env_per_port: float = 0.01,
    pinched_pairs: int = 0,
) -> Dict[str, float]:
    """
    Compare predicted interferometer fringe visibility V across:
      1. Standard QM (only smooth technical noise Gamma_env = gamma_env_per_port * N)
      2. Mass-Proportional Collapse (CSL/DP: Gamma_CSL ~ (M / 10^4 amu)^2, independent of rank)
      3. CFR Freedom-Rank Decoherence (Gamma_CFR depends on rank G^(L), NOT physical N or M!)
    """
    fg = build_n_port_interferometer_graph(n_ports=n_ports, pinched_pairs=pinched_pairs)
    effective_rank = fg.rank()

    gamma_env = gamma_env_per_port * n_ports
    gamma_csl = 0.05 * ((mass_amu / 1.0e4) ** 2)
    gamma_cfr = CFRPredictions.threshold_decoherence(
        rank_F=effective_rank,
        rank_c=rank_c,
        gamma_star=gamma_star,
        power=1.0,
    )

    v_qm = math.exp(-gamma_env * dwell_time)
    v_csl = math.exp(-(gamma_env + gamma_csl) * dwell_time)
    v_cfr = math.exp(-(gamma_env + gamma_cfr) * dwell_time)

    return {
        "n_ports": float(n_ports),
        "pinched_pairs": float(pinched_pairs),
        "effective_rank_F": float(effective_rank),
        "mass_amu": mass_amu,
        "V_QM": v_qm,
        "V_CSL": v_csl,
        "V_CFR": v_cfr,
    }


def demo() -> None:
    print("=== CFR Predictions: Multi-Path High-Rank Interferometry Protocol ===")
    print("1) Photon sweep (M = 0 amu, critical rank R_c = 4):")
    for n in (2, 4, 6, 8):
        r = compare_competing_theories(n_ports=n, mass_amu=0.0, rank_c=4)
        print(
            f"   N={n:2d} (rank={int(r['effective_rank_F']):2d}): "
            f"V_QM={r['V_QM']:.4f}  V_CSL={r['V_CSL']:.4f}  V_CFR={r['V_CFR']:.4f}"
        )

    print("2) Macromolecule 2-slit check (M = 25,000 amu, N = 2 < R_c = 4):")
    macro = compare_competing_theories(n_ports=2, mass_amu=25000.0, rank_c=4)
    print(
        f"   V_QM={macro['V_QM']:.4f}  V_CSL={macro['V_CSL']:.4f} (suppressed)  "
        f"V_CFR={macro['V_CFR']:.4f} (unsuppressed!)"
    )

    print("3) Soft-Roadblock Pinching Control at N = 6 physical ports (R_c = 4):")
    open6 = compare_competing_theories(n_ports=6, mass_amu=0.0, rank_c=4, pinched_pairs=0)
    pinch6 = compare_competing_theories(n_ports=6, mass_amu=0.0, rank_c=4, pinched_pairs=2)
    print(f"   Unpinched (rank 6 > 4): V_CFR={open6['V_CFR']:.4f}")
    print(f"   Pinched   (rank 4 <= 4): V_CFR={pinch6['V_CFR']:.4f} == V_QM={pinch6['V_QM']:.4f}")


if __name__ == "__main__":
    demo()
