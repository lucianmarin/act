"""
Automated Verification Suite for Pure CFR (Constraint-Freedom-Roadblock) Proofs & Models.

Tests every theorem and conditional derivation in `cfr/cfr-proofs.md` across
`models/model_m0.py` .. `models/model_m5.py` and `models/predictions.py`
using only the Python standard library.
"""

from __future__ import annotations

import math
import unittest

from models.model_m0 import (
    ActionHistory,
    CFRActionSystem,
    build_congruence_counterexample,
    check_periodic_matter_knot,
)
from models.model_m1 import (
    Action,
    FiniteActionModel,
    build_bipartite_action_experiment,
    build_model_m1,
    gauge_transform,
    verify_born_rule_exponent,
)
from models.model_m2 import (
    FreedomGeometry,
    build_roadblock_zoo,
    fubini_study_metric,
    max_matrix_diff,
)
from models.model_m3 import (
    CausalDiamondMetric,
    verify_kinematic_roadblock_cone,
)
from models.model_m4 import CFRMatterPattern
from models.model_m5 import (
    FreedomDefectGravity,
    NonAbelianFiberPlaquette,
    mat_expm,
    mat_scale,
)
from models.predictions import (
    CFRPredictions,
    compare_competing_theories,
    fringe_visibility,
    kraus_roadblock_step,
)


class TestM0PureCFR(unittest.TestCase):
    """Verify Section 2: Pure CFR Action Systems, State Emergence, and Causal Posets."""

    def test_prefix_closure_axiom_enforced(self) -> None:
        raw_sys = CFRActionSystem(["a", "b"], [("a", "b")], enforce_closure=False)
        self.assertFalse(raw_sys.verify_subhistory_closure())
        closed_sys = CFRActionSystem(["a", "b"], [("a", "b")], enforce_closure=True)
        self.assertTrue(closed_sys.verify_subhistory_closure())

    def test_one_step_fails_congruence_while_full_cone_succeeds(self) -> None:
        sys = build_congruence_counterexample()
        ha = ActionHistory(("a",))
        hb = ActionHistory(("b",))
        # Proposition 2.1: N_1(a) == N_1(b) == {'c'}, yet (c o a) !~_1 (c o b)
        self.assertEqual(sys.continuations_1(ha), frozenset({"c"}))
        self.assertEqual(sys.continuations_1(hb), frozenset({"c"}))
        self.assertTrue(sys.one_step_equivalent(ha, hb))
        self.assertFalse(sys.one_step_equivalent(ha.extend("c"), hb.extend("c")))

        # Theorem 2.3: Myhill-Nerode full-cone relation ~ is an exact congruence
        self.assertFalse(sys.future_equivalent(ha, hb))
        self.assertTrue(sys.verify_left_congruence())

        # Distinct terminal histories ("a","c","d") and ("b","c") merge into 1 Hard Roadblock state
        h_term1 = ActionHistory(("a", "c", "d"))
        h_term2 = ActionHistory(("b", "c"))
        self.assertTrue(sys.is_hard_roadblock(h_term1))
        self.assertTrue(sys.is_hard_roadblock(h_term2))
        self.assertTrue(sys.future_equivalent(h_term1, h_term2))

        states, trans = sys.state_transitions()
        self.assertGreaterEqual(len(states), 3)
        self.assertGreater(len(trans), 0)
        self.assertTrue(sys.verify_causal_strict_partial_order())

    def test_periodic_matter_knot_emerges_from_finite_cycles(self) -> None:
        knot = check_periodic_matter_knot(period_steps=3, max_cycles=4)
        self.assertTrue(knot["periodic_state_preserved"])


class TestM1QuantumAction(unittest.TestCase):
    """Verify Section 4: Interference, U(1) Gauge Invariance, Born Exponent, and Entanglement."""

    def test_double_slit_interference_and_u1_rephasing(self) -> None:
        constructive = build_model_m1(theta=0.0)
        destructive = build_model_m1(theta=math.pi)
        self.assertAlmostEqual(constructive.transition_probability("i", "f"), 1.0, places=12)
        self.assertAlmostEqual(destructive.transition_probability("i", "f"), 0.0, places=12)

        # Local U(1) gauge transform preserves all observable probabilities
        phases = {"i": 0.3, "a": -1.4, "b": 2.1, "f": 0.9, "x": -0.7, "y": 1.2}
        gauged = gauge_transform(constructive, phases)
        for dst in ("a", "b", "f"):
            self.assertAlmostEqual(
                constructive.transition_probability("i", dst),
                gauged.transition_probability("i", dst),
                places=12,
            )

    def test_born_rule_exponent_uniquely_two(self) -> None:
        # Theorem 4.2: alpha = 2 uniquely conserves probability across two-stage interferometers
        res_2 = verify_born_rule_exponent(2.0)
        self.assertLess(abs(res_2["conservation_error"]), 1e-14)
        for bad_alpha in (1.0, 1.5, 2.5, 3.0, 4.0):
            res_bad = verify_born_rule_exponent(bad_alpha)
            self.assertGreater(abs(res_bad["conservation_error"]), 0.1)

    def test_bipartite_entanglement_and_no_signalling(self) -> None:
        ent_0 = build_bipartite_action_experiment(entangled=True, phi_a=0.0)
        ent_shifted = build_bipartite_action_experiment(entangled=True, phi_a=1.37)
        sep = build_bipartite_action_experiment(entangled=False, phi_a=0.0)
        self.assertEqual(ent_0["rank"], 2)
        self.assertEqual(sep["rank"], 1)
        # Local phase action on subsystem A cannot signal to subsystem B marginals
        self.assertAlmostEqual(ent_0["marginal_B0"], ent_shifted["marginal_B0"], places=12)
        self.assertAlmostEqual(ent_0["marginal_B1"], ent_shifted["marginal_B1"], places=12)


class TestM2FreedomGeometry(unittest.TestCase):
    """Verify Section 3: Canonical Freedom Metric G_AB, Gauge Invariance, and Roadblock Rank Theorem."""

    def test_roadblock_zoo_classification_and_gauge_invariance(self) -> None:
        zoo = build_roadblock_zoo()

        reg = zoo["regular"]
        self.assertEqual(reg.rank(), 2)
        self.assertGreater(reg.det(), 0.1)
        self.assertGreater(reg.freedom_volume(), 0.3)
        self.assertEqual(reg.classify_regime(), "regular")

        phases = {"h": 0.7, "a": -1.2, "b": 2.4, "x1": 0.5, "x2": -0.9}
        reg_gauged = FreedomGeometry(gauge_transform(reg.model, phases), "h", horizon=2)
        self.assertLess(max_matrix_diff(reg.G, reg_gauged.G), 1e-14)
        self.assertAlmostEqual(reg.freedom_volume(), reg_gauged.freedom_volume(), places=14)

        hard = zoo["hard"]
        self.assertEqual(hard.rank(), 0)
        self.assertEqual(hard.classify_regime(), "hard_roadblock")

        inter = zoo["interference"]
        self.assertEqual(len(inter.initial_actions), 2)
        self.assertEqual(inter.rank(), 1)
        self.assertAlmostEqual(inter.freedom_volume(), 0.0, places=12)
        self.assertEqual(inter.classify_regime(), "interference_roadblock")

        coll = zoo["collinear"]
        self.assertEqual(len(coll.initial_actions), 2)
        self.assertEqual(coll.rank(), 1)
        self.assertAlmostEqual(coll.det(), 0.0, places=12)
        self.assertAlmostEqual(coll.freedom_volume(), 0.0, places=12)
        self.assertEqual(coll.classify_regime(), "collinear_roadblock")

    def test_fubini_study_smooth_limit(self) -> None:
        theta = 0.9
        phi = 0.4
        psi_fn = lambda p: [
            math.cos(p[0] / 2.0) + 0j,
            complex(math.cos(p[1]), math.sin(p[1])) * math.sin(p[0] / 2.0),
        ]
        g_fs = fubini_study_metric(psi_fn, [theta, phi])
        self.assertAlmostEqual(g_fs[0][0], 0.25, places=7)
        self.assertAlmostEqual(g_fs[1][1], 0.25 * (math.sin(theta) ** 2), places=7)
        self.assertAlmostEqual(g_fs[0][1], 0.0, places=7)


class TestM3CausalLorentzian(unittest.TestCase):
    """Verify Section 2.5 and Section 5: Kinematic Roadblock Cones and Lorentzian (-+++) Metric."""

    def test_kinematic_roadblock_light_cone(self) -> None:
        res = verify_kinematic_roadblock_cone(max_steps=3)
        self.assertEqual(res["max_outside_cone_amp"], 0.0)
        self.assertGreater(res["max_inside_cone_amp"], 0.0)
        self.assertTrue(res["spacelike_no_signalling"])
        self.assertTrue(res["timelike_influence_present"])

    def test_causal_diamond_boost_invariance_and_signature(self) -> None:
        geom = CausalDiamondMetric(c=2.0)
        tau0 = geom.proper_ticks_from_counts(8.0, 2.0)
        t_val, x_val = geom.coords_from_counts(8.0, 2.0)
        self.assertAlmostEqual(tau0, math.sqrt(t_val ** 2 - (x_val / 2.0) ** 2), places=12)

        for eta in (-1.5, -0.4, 0.7, 1.9):
            np_b, nm_b = geom.boost_counts(8.0, 2.0, eta)
            self.assertAlmostEqual(geom.proper_ticks_from_counts(np_b, nm_b), tau0, places=12)

        # Vanishes on null Kinematic Roadblock (N_- = 0) and rejects outside cone (N_- < 0)
        self.assertEqual(geom.proper_ticks_from_counts(5.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            geom.proper_ticks_from_counts(5.0, -0.1)

        g_mat = geom.extract_metric_tensor_hessian()
        neg, pos = geom.signature_counts(g_mat)
        self.assertEqual((neg, pos), (1, 3))
        self.assertAlmostEqual(g_mat[0][0], -4.0, places=5)  # -c^2 = -4.0
        self.assertAlmostEqual(g_mat[1][1], 1.0, places=5)


class TestM4MassEnergy(unittest.TestCase):
    """Verify Corollary 5.3 and research/mass-energy-equivalence.md: E_0 = mc^2 and E^2 = p^2c^2 + m^2c^4."""

    def test_stiffness_inertial_mass_and_relativistic_dispersion(self) -> None:
        for mu, c_val in ((1.5, 1.0), (2.75, 3.0)):
            knot = CFRMatterPattern(stiffness_mu=mu, c=c_val)
            self.assertAlmostEqual(knot.inertial_mass(), mu, places=5)
            for frac in (0.0, 0.25, 0.6, 0.85):
                chk = knot.verify_dispersion_and_equivalence(v=frac * c_val)
                self.assertLess(chk["rest_equivalence_error"], 1e-5)
                self.assertLess(chk["dispersion_error"], 1e-4)

            ann = knot.annihilate_to_null_modes(v=0.5 * c_val)
            self.assertLess(ann["energy_conservation_err"], 1e-12)
            self.assertLess(ann["momentum_conservation_err"], 1e-12)
            self.assertGreater(ann["E_gamma_plus"], ann["E_gamma_minus"])


class TestM5GaugeAndGravity(unittest.TestCase):
    """Verify Section 6 (U(n) Gauge Fibers) and Section 7.2 (Gravitational Defect K_mu_nu)."""

    def test_u_n_plaquette_gauge_invariance_and_yang_mills_continuum(self) -> None:
        for rank_n in (2, 3):
            r_coarse = NonAbelianFiberPlaquette.verify_nonabelian_gauge_and_bch(
                n=rank_n, eps=2e-3
            )
            r_fine = NonAbelianFiberPlaquette.verify_nonabelian_gauge_and_bch(
                n=rank_n, eps=1e-3
            )
            self.assertLess(r_fine["gauge_invariance_err"], 1e-13)
            self.assertGreater(r_fine["non_abelian_commutator_norm"], 0.1)
            # First-order O(eps) convergence to exact continuum Yang-Mills curvature F_mu_nu
            self.assertLess(r_fine["yang_mills_bch_err"], 0.6 * r_coarse["yang_mills_bch_err"])

    def test_freedom_defect_tensor_gr_limit_bianchi_and_roadblock_surge(self) -> None:
        # 1. Constant G_AB => K_mu_nu == 0 (exact GR limit)
        k_const = FreedomDefectGravity.compute_K_tensor(
            lambda pt: [[3.0 + 0j, 0.5j], [-0.5j, 2.0 + 0j]],
            [0.1, -0.2, 0.3, 0.4],
        )
        self.assertLess(max(abs(v) for row in k_const for v in row), 1e-13)

        # 2. Plane-wave harmonic solution G(x) = exp(H sin(t - x)) satisfies d^mu K_mu_nu == 0
        h_mat = [[0.8 + 0j, 0.3 - 0.1j], [0.3 + 0.1j, -0.5 + 0j]]
        wave = lambda pt: mat_expm(mat_scale(h_mat, 0.4 * math.sin(pt[0] - pt[1])))
        div_k = FreedomDefectGravity.divergence_K(wave, [0.25, -0.15, 0.0, 0.0])
        self.assertLess(max(abs(d) for d in div_k), 1e-5)

        # 3. Soft-Roadblock pinching lambda_1(x) = x -> 0^+ gives 1/x^2 inverse-square surge
        pinch = lambda pt: [[pt[1] + 0j, 0j], [0j, 1.0 + 0j]]
        k_01 = FreedomDefectGravity.compute_K_tensor(pinch, [0.0, 0.1, 0.0, 0.0])[1][1]
        k_001 = FreedomDefectGravity.compute_K_tensor(pinch, [0.0, 0.01, 0.0, 0.0])[1][1]
        self.assertAlmostEqual(k_001 / k_01, 100.0, delta=0.05)

        # 4. Non-minimal coupling xi_F < 0 creates negative null-energy contribution near convex pinch
        convex_pinch = lambda pt: [[math.exp(pt[1] ** 2) + 0j, 0j], [0j, 1.0 + 0j]]
        k_defocus = FreedomDefectGravity.compute_K_tensor(
            convex_pinch, [0.0, 0.0, 0.0, 0.0], xi_F=-0.5, lambda_F=1.0
        )
        null_projection = k_defocus[0][0] + k_defocus[1][1]  # K_{mu nu} k^mu k^nu for k=(1,1,0,0)
        self.assertLess(null_projection, -0.5)


class TestPredictionsProtocol(unittest.TestCase):
    """Verify Section 7.1 (Kraus Roadblock Channel) and Section 8 (Multi-Path Protocol)."""

    def test_kraus_step_unitarity_below_rc_and_decoherence_above_rc(self) -> None:
        n = 5
        rho0 = [[1.0 / n + 0j for _ in range(n)] for _ in range(n)]
        self.assertAlmostEqual(fringe_visibility(rho0), 1.0, places=12)

        # Below critical rank R_c = 5: exact unitary preservation
        rho_below = kraus_roadblock_step(rho0, rank_F=5, rank_c=5, gamma_0=0.4, dt=0.5)
        self.assertAlmostEqual(fringe_visibility(rho_below), 1.0, places=12)

        # Above critical rank R_c = 3: trace preserved, fringe visibility strictly reduced
        rho_above = kraus_roadblock_step(rho0, rank_F=5, rank_c=3, gamma_0=0.4, dt=0.5)
        tr = sum(rho_above[i][i].real for i in range(n))
        self.assertAlmostEqual(tr, 1.0, places=12)
        self.assertLess(fringe_visibility(rho_above), 0.95)

    def test_three_way_experimental_discrimination_and_pinching_control(self) -> None:
        # 1. Zero-mass photon above R_c: CSL agrees with QM, CFR predicts anomalous drop
        photon_high = compare_competing_theories(n_ports=8, mass_amu=0.0, rank_c=4)
        self.assertAlmostEqual(photon_high["V_CSL"], photon_high["V_QM"], places=12)
        self.assertLess(photon_high["V_CFR"], 0.6 * photon_high["V_QM"])

        # 2. Massive molecule below R_c: CFR agrees with QM, CSL predicts collapse
        heavy_2slit = compare_competing_theories(n_ports=2, mass_amu=30000.0, rank_c=4)
        self.assertAlmostEqual(heavy_2slit["V_CFR"], heavy_2slit["V_QM"], places=12)
        self.assertLess(heavy_2slit["V_CSL"], 0.7 * heavy_2slit["V_QM"])

        # 3. Soft-Roadblock Pinching Control: 6 physical arms pinched to rank 4 restores QM visibility
        unpinched = compare_competing_theories(n_ports=6, mass_amu=0.0, rank_c=4, pinched_pairs=0)
        pinched = compare_competing_theories(n_ports=6, mass_amu=0.0, rank_c=4, pinched_pairs=2)
        self.assertEqual(unpinched["effective_rank_F"], 6.0)
        self.assertEqual(pinched["effective_rank_F"], 4.0)
        self.assertLess(unpinched["V_CFR"], pinched["V_CFR"])
        self.assertAlmostEqual(pinched["V_CFR"], pinched["V_QM"], places=12)


if __name__ == "__main__":
    unittest.main()
