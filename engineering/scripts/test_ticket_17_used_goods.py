#!/usr/bin/env python3
"""Test suite for Ticket 17: Make used/discontinued recommendations category-aware.
Tests:
1. Pass: Camera body is admissible with specialized camera checklist (shutter count, CMOS scan).
2. Pass: Baby car seat is strictly restricted due to hidden collision history risk.
3. Pass: 6-year-old discontinued product includes EOL driver and consumable trade-off.
4. Adversarial: Laptop checklist MUST NOT contain camera shutter count or optical glass inspection.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from used_goods_evaluator import evaluate_used_product_eligibility

class TestTicket17UsedGoods(unittest.TestCase):
    def test_01_camera_admissible_with_specialized_checklist(self):
        """Pass path: Camera category admits used with dedicated camera checklist."""
        res = evaluate_used_product_eligibility(
            category="camera_body",
            product_model="Pro Camera Mark III",
            release_year=2023,
            current_year=2026
        )
        self.assertEqual(res["eligibility"], "admissible")
        self.assertTrue(res["recommended_for_used"])
        checklist_str = " ".join(res["checklist"]).lower()
        self.assertIn("shutter actuation count", checklist_str)
        self.assertIn("cmos sensor", checklist_str)

    def test_02_baby_car_seat_restricted_for_hidden_collision_risk(self):
        """Pass path: Child car seat is strictly discouraged/restricted due to unseen collision history."""
        res = evaluate_used_product_eligibility(
            category="baby_car_seat",
            product_model="Infant Shield 360",
            release_year=2024,
            current_year=2026
        )
        self.assertEqual(res["eligibility"], "restricted_safety_hazard")
        self.assertFalse(res["recommended_for_used"])
        self.assertIn("collision history", res["safety_restriction_rationale"])
        self.assertEqual(len(res["checklist"]), 0)

    def test_03_discontinued_product_includes_eol_tradeoff(self):
        """Pass path: 6-year-old product (released 2020) evaluates OS driver and consumable supply."""
        res = evaluate_used_product_eligibility(
            category="laptop_workstation",
            product_model="ThinkPad Classic 2020",
            release_year=2020,
            current_year=2026,
            eol_support_status={"driver_support": "Win10 only, no Win11 official driver", "consumable_status": "OEM batteries out of stock"}
        )
        self.assertEqual(res["eligibility"], "admissible")
        self.assertIsNotNone(res["eol_tradeoff"])
        self.assertEqual(res["eol_tradeoff"]["age_years"], 6)
        self.assertIn("Win10 only", res["eol_tradeoff"]["driver_os_compatibility_warning"])

    def test_04_adversarial_checklist_isolation_no_shutter_count_on_laptop(self):
        """Adversarial path: Laptop category checklist must never leak camera shutter count items."""
        res = evaluate_used_product_eligibility(
            category="laptop_workstation",
            product_model="Developer Laptop X1",
            release_year=2024,
            current_year=2026
        )
        self.assertEqual(res["matched_category"], "laptop_workstation")
        checklist_str = " ".join(res["checklist"]).lower()
        
        # Must contain laptop items
        self.assertIn("battery health", checklist_str)
        self.assertIn("mdm enterprise", checklist_str)
        
        # Must strictly NOT contain camera items
        self.assertNotIn("shutter", checklist_str)
        self.assertNotIn("cmos", checklist_str)
        self.assertNotIn("lens mount", checklist_str)

if __name__ == "__main__":
    unittest.main()
