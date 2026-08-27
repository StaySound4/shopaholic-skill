#!/usr/bin/env python3
"""Test suite for Ticket 19: Add cross-border landed-cost and compatibility treatment.
Tests:
1. Pass: Deterministic arithmetic ($500 product + $30 shipping + $50 tax at FX 7.00 = CNY 4060.00).
2. Pass: Destination safety certifications (UL, ETL, CE, PSE) are verified.
3. Pass: Non-monetary regional risks (110V voltage, voided warranty, missing 3C, cloud locks, return friction) disclosed.
4. Pass: Keepa historical tracking detects inflated list prices and fake promotional discounts.
5. Pass: ASIN review hijacking (swapped reviews from unrelated categories) is detected and filtered.
6. Adversarial: Unknown import tax or shipping MUST NOT be silently set to zero (returns is_complete=False).
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from landed_cost_engine import (
    calculate_cross_border_landed_cost,
    verify_destination_safety_certifications,
    evaluate_cross_border_regional_risks,
    analyze_overseas_price_history,
    detect_asin_review_hijacking
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
            tax_status="known",
            shipping_status="known"
        )
        self.assertTrue(res["is_complete"])
        self.assertEqual(res["total_foreign_cost"], 580.0)
        self.assertEqual(res["landed_cost_cny"], 4060.00)
        self.assertIsNone(res["risk_warning"])

    def test_02_destination_safety_certifications(self):
        """Pass path: Destination certifications (UL, ETL, CE, PSE) are strictly verified."""
        res = verify_destination_safety_certifications(
            product_model="Global PSU 850W",
            destination_region="US",
            claimed_certifications=["UL", "FCC"],
            official_registry_certs=["UL", "FCC"]
        )
        self.assertTrue(res["is_safety_compliant"])
        self.assertIn("UL", res["verified_certifications"])

    def test_03_regional_compatibility_and_warranty_risks(self):
        """Pass path: US 110V appliance discloses voltage, warranty, 3C, cloud locks, and return friction."""
        risks_res = evaluate_cross_border_regional_risks(
            product_model="US Stand Mixer Pro",
            origin_market="US",
            destination_market="CN",
            voltage="110V",
            plug_type="Type A/B (US)",
            has_domestic_warranty=False,
            has_domestic_3c=False,
            has_regional_cloud_lock=True,
            has_high_return_friction=True,
            seller_tier="sold_and_shipped_by_retailer"
        )
        risk_types = [r["risk_type"] for r in risks_res["disclosed_risks"]]
        self.assertIn("voltage_incompatibility", risk_types)
        self.assertIn("voided_domestic_warranty", risk_types)
        self.assertIn("missing_domestic_ccc", risk_types)
        self.assertIn("regional_cloud_lock", risk_types)
        self.assertIn("high_cross_border_return_friction", risk_types)

    def test_04_keepa_inflated_msrp_detection(self):
        """Pass path: Identifies artificial deal markups where MSRP was inflated before sale."""
        res = analyze_overseas_price_history(
            current_list_price=180.0,
            claimed_original_msrp=350.0,
            historical_90day_median_price=200.0
        )
        self.assertTrue(res["is_msrp_inflated"])
        self.assertEqual(res["true_discount_vs_90day_median_pct"], 10.0)
        self.assertIn("Fake discount", res["notes"])

    def test_05_asin_review_hijacking_detection(self):
        """Pass path: Filters ASIN variation hijacking where reviews belong to different categories."""
        reviews = [
            {"reviewer": "alice", "reviewed_product_name": "Silicon Phone Case", "rating": 5},
            {"reviewer": "bob", "reviewed_product_name": "High-Power Kitchen Blender", "rating": 4}
        ]
        res = detect_asin_review_hijacking(
            current_product_asin="B00EXAMPLE",
            current_product_category="blender",
            top_reviews=reviews
        )
        self.assertTrue(res["is_review_hijacked"])
        self.assertEqual(res["hijacked_review_count"], 1)
        self.assertEqual(res["legitimate_review_count"], 1)

    def test_06_adversarial_unknown_tax_or_shipping_cannot_be_silently_zeroed(self):
        """Adversarial path: Unknown tax or unknown shipping cannot be treated as 0.0."""
        # Case A: Unknown tax
        res_tax = calculate_cross_border_landed_cost(
            product_price=500.0,
            currency="USD",
            fx_rate_to_cny=7.00,
            international_shipping=30.0,
            import_duty_tax=None,
            tax_status="unknown"
        )
        self.assertFalse(res_tax["is_complete"])
        self.assertIsNone(res_tax["landed_cost_cny"])
        self.assertIn("customs tax is unknown", res_tax["risk_warning"])

        # Case B: Unknown shipping
        res_ship = calculate_cross_border_landed_cost(
            product_price=500.0,
            currency="USD",
            fx_rate_to_cny=7.00,
            international_shipping=None,
            import_duty_tax=50.0,
            shipping_status="unknown"
        )
        self.assertFalse(res_ship["is_complete"])
        self.assertIsNone(res_ship["landed_cost_cny"])
        self.assertIn("shipping cost is unknown", res_ship["risk_warning"])

if __name__ == "__main__":
    unittest.main()
