#!/usr/bin/env python3
"""Test suite for Ticket 25: Implement deterministic sensitivity flip-point analysis.
Tests:
1. Pass: Two-criterion fixture A=(90,60), B=(70,90) computes exact mathematical flip point w_1=0.4.
2. Pass: Generates natural language contextual scenario slider without ungrounded pseudo-probability.
3. Pass: Articulates pairwise dominant trade-off margins.
4. Adversarial: Pareto dominance (A strictly better on all criteria) strictly suppresses sensitivity analysis.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sensitivity_engine import (
    compute_linear_flip_point,
    analyze_candidate_sensitivity
)

class TestTicket25Sensitivity(unittest.TestCase):
    def test_01_deterministic_exact_flip_point(self):
        """Pass path: Two-criterion fixture computes exact flip weight w_1=0.4."""
        # A=(90, 60), B=(70, 90)
        # delta_0 = 90 - 70 = 20
        # delta_1 = 90 - 60 = 30
        # w_1* = 20 / (20 + 30) = 0.4
        w_flip = compute_linear_flip_point(score_a_0=90.0, score_a_1=60.0, score_b_0=70.0, score_b_1=90.0)
        self.assertIsNotNone(w_flip)
        self.assertAlmostEqual(w_flip, 0.4, places=4)

    def test_02_contextual_scenario_slider_generation(self):
        """Pass path: Sensitivity analysis outputs natural language scenario slider."""
        cand_a = {"name": "Camera Alpha", "scores": {"photo": 90.0, "video": 60.0}}
        cand_b = {"name": "Camera Beta", "scores": {"photo": 70.0, "video": 90.0}}
        
        res = analyze_candidate_sensitivity(
            candidate_a=cand_a,
            candidate_b=cand_b,
            criterion_0="photo",
            criterion_1="video",
            criterion_0_label="Still Photography",
            criterion_1_label="Video Recording"
        )
        
        self.assertFalse(res["suppressed"])
        self.assertAlmostEqual(res["flip_weight_criterion_1"], 0.4, places=4)
        self.assertAlmostEqual(res["flip_weight_criterion_0"], 0.6, places=4)
        
        slider = res["contextual_slider"]
        self.assertIn("Still Photography priority >= 60%", slider)
        self.assertIn("Camera Alpha is the optimal choice", slider)
        self.assertIn("Video Recording priority exceeds 40%", slider)
        self.assertIn("Camera Beta", slider)

    def test_03_pairwise_tradeoff_margins(self):
        """Pass path: Pairwise trade-off margins are accurately articulated."""
        cand_a = {"name": "Display A", "scores": {"refresh_rate": 100.0, "color_accuracy": 70.0}}
        cand_b = {"name": "Display B", "scores": {"refresh_rate": 60.0, "color_accuracy": 95.0}}
        
        res = analyze_candidate_sensitivity(
            candidate_a=cand_a,
            candidate_b=cand_b,
            criterion_0="refresh_rate",
            criterion_1="color_accuracy"
        )
        self.assertFalse(res["suppressed"])
        self.assertEqual(res["pairwise_tradeoff"]["advantage_crit0"]["winner"], "Display A")
        self.assertEqual(res["pairwise_tradeoff"]["advantage_crit0"]["margin"], 40.0)
        self.assertEqual(res["pairwise_tradeoff"]["advantage_crit1"]["winner"], "Display B")
        self.assertEqual(res["pairwise_tradeoff"]["advantage_crit1"]["margin"], 25.0)

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

if __name__ == "__main__":
    unittest.main()
