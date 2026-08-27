#!/usr/bin/env python3
"""Test suite for Ticket 26: Make cost-of-pivot analysis conditional by changed architecture.
Tests:
1. Pass: Action camera -> vehicle-mounted 360 panoramic camera triggers full relevant 4D pivot costs.
2. Pass: Air cooling -> open-loop liquid cooling triggers workflow/safety costs while omitting irrelevant compute dimension.
3. Adversarial: Cosmetic black -> white color change strictly suppresses pivot cost analysis.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pivot_cost_engine import evaluate_cost_of_pivot

class TestTicket26PivotCost(unittest.TestCase):
    def test_01_action_cam_to_360_pivot_triggers_4d_costs(self):
        """Pass path: Standard action camera to 360 camera triggers 4D transfer costs."""
        res = evaluate_cost_of_pivot(
            baseline_architecture="standard_action_camera",
            target_architecture="360_panoramic_camera"
        )
        self.assertTrue(res["pivot_triggered"])
        self.assertEqual(res["dimension_count"], 4)
        
        pivot_cost = res["pivot_cost"]
        self.assertIn("workflow_friction", pivot_cost)
        self.assertIn("kinetic_ergonomic_safety", pivot_cost)
        self.assertIn("compute_ecosystem", pivot_cost)
        self.assertIn("fragility_tco", pivot_cost)
        self.assertIn("stitching", pivot_cost["workflow_friction"])
        self.assertIn("fisheye", pivot_cost["kinetic_ergonomic_safety"])

    def test_02_cooling_pivot_omits_irrelevant_dimension(self):
        """Pass path: Air cooling to open-loop water cooling omits irrelevant compute dimension."""
        res = evaluate_cost_of_pivot(
            baseline_architecture="traditional_air_cooling",
            target_architecture="custom_open_loop_liquid"
        )
        self.assertTrue(res["pivot_triggered"])
        pivot_cost = res["pivot_cost"]
        self.assertIn("workflow_friction", pivot_cost)
        self.assertIn("kinetic_ergonomic_safety", pivot_cost)
        self.assertNotIn("compute_ecosystem", pivot_cost)  # Omitted as irrelevant

    def test_03_adversarial_cosmetic_color_swap_suppresses_analysis(self):
        """Adversarial path: Pure cosmetic color swap (black to white) must not trigger pivot cost analysis."""
        res = evaluate_cost_of_pivot(
            baseline_architecture="standard_action_camera",
            target_architecture="standard_action_camera",
            baseline_attributes={"color": "matte_black", "finish": "rubberized"},
            target_attributes={"color": "glacier_white", "finish": "rubberized"}
        )
        self.assertFalse(res["pivot_triggered"])
        self.assertIsNone(res["pivot_cost"])
        self.assertIn("cosmetic/preference variation", res["reason"])

if __name__ == "__main__":
    unittest.main()
