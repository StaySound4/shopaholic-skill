#!/usr/bin/env python3
"""Test suite for Ticket 25: Implement deterministic sensitivity flip-point analysis.
Tests:
1. Pass: Two-criterion fixture A=(90,60), B=(70,90) computes exact mathematical flip point w_1=0.4.
2. Pass: Generates natural language contextual scenario slider and records input metadata + normalization rules.
3. Pass: Articulates pairwise dominant trade-off margins and handles 3-candidate rivalries.
4. Adversarial: Pareto dominance (A strictly better on all criteria) strictly suppresses sensitivity analysis.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sensitivity_engine import (
    compute_linear_flip_point,
    analyze_candidate_sensitivity,
    analyze_three_candidate_rivalry
)

class TestTicket25Sensitivity(unittest.TestCase):
    def test_01_deterministic_exact_flip_point(self):
        """Pass path: Two-criterion fixture computes exact flip weight w_1=0.4."""
        w_flip = compute_linear_flip_point(score_a_0=90.0, score_a_1=60.0, score_b_0=70.0, score_b_1=90.0)
        self.assertIsNotNone(w_flip)
        self.assertAlmostEqual(w_flip, 0.4, places=4)

    def test_02_contextual_scenario_slider_and_input_recording(self):
        """Pass path: Sensitivity analysis outputs scenario slider and records input metadata."""
        cand_a = {"name": "Camera Alpha", "scores": {"photo": 90.0, "video": 60.0}}
        cand_b = {"name": "Camera Beta", "scores": {"photo": 70.0, "video": 90.0}}
        
        res = analyze_candidate_sensitivity(
            candidate_a=cand_a,
            candidate_b=cand_b,
            criterion_0="photo",
            criterion_1="video",
            criterion_0_label="Still Photography",
            criterion_1_label="Video Recording",
            normalization_rule="linear_0_to_100"
        )
        
        self.assertFalse(res["suppressed"])
        self.assertAlmostEqual(res["flip_weight_criterion_1"], 0.4, places=4)
        self.assertAlmostEqual(res["flip_weight_criterion_0"], 0.6, places=4)
        
        # Verify inputs and normalization rule are recorded
        self.assertIn("inputs_recorded", res)
        self.assertEqual(res["inputs_recorded"]["normalization_rule"], "linear_0_to_100")
        self.assertEqual(res["inputs_recorded"]["candidate_a"]["scores"]["photo"], 90.0)
        
        slider = res["contextual_slider"]
        self.assertIn("Still Photography priority >= 60%", slider)
        self.assertIn("Camera Alpha is the optimal choice", slider)

    def test_03_three_candidate_rivalry_pairwise_analysis(self):
        """Pass path: 3-candidate rivalry evaluates all pairwise trade-off flip points."""
        cand_a = {"name": "Cam A", "scores": {"photo": 90.0, "video": 60.0}}
        cand_b = {"name": "Cam B", "scores": {"photo": 70.0, "video": 90.0}}
        cand_c = {"name": "Cam C", "scores": {"photo": 80.0, "video": 75.0}}
        
        res_3way = analyze_three_candidate_rivalry(
            candidates=[cand_a, cand_b, cand_c],
            criterion_0="photo",
            criterion_1="video"
        )
        
        self.assertEqual(res_3way["rivalry_type"], "three_candidate_pairwise_tradeoffs")
        self.assertEqual(len(res_3way["pairwise_analyses"]), 3)
        self.assertEqual(res_3way["candidate_names"], ["Cam A", "Cam B", "Cam C"])

    def test_04_adversarial_pareto_dominance_suppresses_analysis(self):
        """Adversarial path: Pareto dominance strictly suppresses sensitivity analysis."""
        cand_a = {"name": "Dominant Option", "scores": {"perf": 95.0, "efficiency": 90.0}}
        cand_b = {"name": "Inferior Option", "scores": {"perf": 70.0, "efficiency": 60.0}}
        
        res = analyze_candidate_sensitivity(
            candidate_a=cand_a,
            candidate_b=cand_b,
            criterion_0="perf",
            criterion_1="efficiency"
        )
        self.assertTrue(res["suppressed"])
        self.assertIsNone(res["flip_weight"])
        self.assertIsNone(res["contextual_slider"])
        self.assertIn("Pareto dominance", res["suppression_reason"])
        self.assertIn("inputs_recorded", res)

if __name__ == "__main__":
    unittest.main()
