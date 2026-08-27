#!/usr/bin/env python3
"""Test suite for Ticket 11: Implement R0-R3 research-budget selection.
Tests both happy path and adversarial conditions:
1. Low-cost mature accessory (69 CNY charger) selects R0 with fast convergence and 2-4 candidates.
2. High-value appliance (20,000 CNY built-in) selects R2 with full provenance and 4D cost analysis.
3. Regulated medical / personal safety device selects R3 with authoritative registry checks.
4. Standard consumer goods select R1.
5. Adversarial path: Low-cost safety-critical product (29 CNY baby bottle) MUST NOT become R0 solely due to price.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_budget_selector import select_research_budget

class TestTicket11Budget(unittest.TestCase):
    def test_01_low_cost_mature_accessory_selects_r0(self):
        """Pass path: 69-yuan phone charger selects R0 with 2-4 candidates and no heavy BOM teardown quota."""
        res = select_research_budget(category="phone_charger", price_cny=69.0)
        self.assertEqual(res["research_budget"], "R0")
        self.assertFalse(res["require_bom_teardown"])
        self.assertLessEqual(res["max_candidate_count"], 4)
        self.assertIn("R0", res["reason"])

    def test_02_high_value_appliance_selects_r2(self):
        """Pass path: 20,000 CNY built-in appliance selects R2."""
        res = select_research_budget(
            category="built_in_dishwasher",
            price_cny=20000.0,
            is_built_in_or_installation_heavy=True
        )
        self.assertEqual(res["research_budget"], "R2")
        self.assertTrue(res["require_bom_teardown"])

    def test_03_medical_and_safety_selects_r3(self):
        """Pass path: Regulated medical device selects R3."""
        res = select_research_budget(
            category="medical_laser_eye_protector",
            price_cny=2500.0,
            is_safety_critical=True
        )
        self.assertEqual(res["research_budget"], "R3")
        self.assertTrue(res["require_regulatory_registry_check"])

    def test_04_standard_consumer_goods_selects_r1(self):
        """Pass path: 899 CNY wireless earbuds select R1."""
        res = select_research_budget(category="wireless_earbuds", price_cny=899.0)
        self.assertEqual(res["research_budget"], "R1")

    def test_05_adversarial_cheap_safety_critical_item_cannot_become_r0(self):
        """Adversarial path: 29 CNY baby feeding bottle has toxicology stakes and must NOT become R0 solely due to low price."""
        res = select_research_budget(
            category="baby_feeding_bottle",
            price_cny=29.0,
            is_safety_critical=True
        )
        
        # Must strictly elevate to R2/R3, never R0
        self.assertNotEqual(res["research_budget"], "R0")
        self.assertIn(res["research_budget"], ["R2", "R3"])
        self.assertTrue(res["require_regulatory_registry_check"])

if __name__ == "__main__":
    unittest.main()
