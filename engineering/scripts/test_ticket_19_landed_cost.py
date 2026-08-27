#!/usr/bin/env python3
"""Test suite for Ticket 19: Add cross-border landed-cost and compatibility treatment.
Tests:
1. Pass: Deterministic arithmetic ($500 product + $30 shipping + $50 tax at FX 7.00 = CNY 4060.00).
2. Pass: Non-monetary regional risks (110V voltage, voided domestic warranty, missing 3C) are explicitly disclosed.
3. Pass: Seller fulfillment tier (FBM) and refurbished condition (Amazon Renewed) are identified.
4. Adversarial: Unknown import tax must NOT be silently set to zero (returns is_complete=False).
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from landed_cost_engine import (
    calculate_cross_border_landed_cost,
    evaluate_cross_border_regional_risks
)

class TestTicket19LandedCost(unittest.TestCase):
    def test_01_deterministic_landed_cost_calculation(self):
        """Pass path: $500 + $30 + $50 at 7.00 produces exactly CNY 4060.00."""
        res = calculate_cross_border_landed_cost(
            product_price=500.0,
            currency="USD",
            fx_rate_to_cny=7.00,
            international_shipping=30.0,
            import_duty_tax=50.0,
            tax_status="known"
        )
        self.assertTrue(res["is_complete"])
        self.assertEqual(res["total_foreign_cost"], 580.0)
        self.assertEqual(res["landed_cost_cny"], 4060.00)
        self.assertIsNone(res["risk_warning"])

    def test_02_regional_compatibility_and_warranty_risks(self):
        """Pass path: US 110V kitchen appliance discloses voltage, warranty, and 3C risks."""
        risks_res = evaluate_cross_border_regional_risks(
            product_model="US Stand Mixer Pro",
            origin_market="US",
            destination_market="CN",
            voltage="110V",
            has_domestic_warranty=False,
            has_domestic_3c=False,
            seller_tier="sold_and_shipped_by_retailer"
        )
        risk_types = [r["risk_type"] for r in risks_res["disclosed_risks"]]
        self.assertIn("voltage_incompatibility", risk_types)
        self.assertIn("voided_domestic_warranty", risk_types)
        self.assertIn("missing_domestic_ccc", risk_types)

    def test_03_seller_tier_and_refurbished_condition(self):
        """Pass path: FBM third-party seller and renewed condition are flagged in risk disclosure."""
        risks_res = evaluate_cross_border_regional_risks(
            product_model="Renewed Laptop",
            origin_market="US",
            seller_tier="third_party_merchant_fbm",
            condition="renewed_refurbished"
        )
        risk_types = [r["risk_type"] for r in risks_res["disclosed_risks"]]
        self.assertIn("high_seller_fulfillment_friction", risk_types)
        self.assertIn("non_new_condition", risk_types)

    def test_04_adversarial_unknown_tax_cannot_be_silently_zeroed(self):
        """Adversarial path: When customs duty is unknown, landed cost cannot be computed as product + 0."""
        res = calculate_cross_border_landed_cost(
            product_price=500.0,
            currency="USD",
            fx_rate_to_cny=7.00,
            international_shipping=30.0,
            import_duty_tax=None,
            tax_status="unknown"
        )
        self.assertFalse(res["is_complete"])
        self.assertIsNone(res["landed_cost_cny"])
        self.assertIsNotNone(res["risk_warning"])
        self.assertIn("unknown", res["risk_warning"])

if __name__ == "__main__":
    unittest.main()
