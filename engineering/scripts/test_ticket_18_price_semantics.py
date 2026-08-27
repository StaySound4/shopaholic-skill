#!/usr/bin/env python3
"""Test suite for Ticket 18: Define strict current, cross-sectional, and historical price semantics.
Tests:
1. Pass: 90-day time-separated observations permit historical time-series range.
2. Pass: Same-day multiple merchant offers are classified as cross-sectional spread, NOT historical trend.
3. Pass: Promotional conditions (trade-in, VIP coupon) are transparently disclosed.
4. Adversarial: Conditional promotion price cannot be presented as unconditional cash price (raises ValueError).
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from price_semantics_engine import (
    PriceObservation,
    analyze_price_observations,
    format_price_display
)

class TestTicket18PriceSemantics(unittest.TestCase):
    def test_01_historical_time_series_range_identified(self):
        """Pass path: Multi-date observations across 90 days form historical range."""
        obs = [
            PriceObservation(product_id="SKU-001", price_amount=2999, observation_date="2026-06-01", channel_seller="JD_Official"),
            PriceObservation(product_id="SKU-001", price_amount=2699, observation_date="2026-06-18", channel_seller="JD_Official"),
            PriceObservation(product_id="SKU-001", price_amount=2899, observation_date="2026-08-28", channel_seller="JD_Official")
        ]
        res = analyze_price_observations(obs)
        self.assertEqual(res["analysis_type"], "historical_time_series_range")
        self.assertTrue(res["is_historical_trend"])
        self.assertEqual(res["date_span_days"], 88)
        self.assertEqual(res["historical_range"]["min"], 2699)
        self.assertEqual(res["historical_range"]["max"], 2999)

    def test_02_same_day_multiple_sellers_classified_as_cross_sectional(self):
        """Pass path: Same-day prices from 3 sellers are classified as cross-sectional spread."""
        obs = [
            PriceObservation(product_id="SKU-001", price_amount=2999, observation_date="2026-08-28", channel_seller="JD_Official"),
            PriceObservation(product_id="SKU-001", price_amount=2899, observation_date="2026-08-28", channel_seller="Tmall_Official"),
            PriceObservation(product_id="SKU-001", price_amount=2750, observation_date="2026-08-28", channel_seller="PDD_BlackLabel")
        ]
        res = analyze_price_observations(obs)
        self.assertEqual(res["analysis_type"], "cross_sectional_spread")
        self.assertFalse(res["is_historical_trend"])
        self.assertEqual(res["seller_count"], 3)
        self.assertEqual(res["price_spread"]["spread"], 249.0)

    def test_03_promotional_conditions_transparently_formatted(self):
        """Pass path: Subsidies and conditions are not silently dropped."""
        obs = PriceObservation(
            product_id="SKU-001",
            price_amount=2399,
            is_unconditional_cash=False,
            conditions=["trade_in_subsidy_400", "bank_installment_discount_100"]
        )
        display = format_price_display(obs)
        self.assertIn("Conditional:", display)
        self.assertIn("trade_in_subsidy_400", display)

    def test_04_adversarial_conditional_cannot_claim_unconditional_cash(self):
        """Adversarial path: Price with coupon/trade-in conditions cannot be marked as unconditional cash."""
        with self.assertRaises(ValueError):
            PriceObservation(
                product_id="SKU-001",
                price_amount=1999,
                is_unconditional_cash=True,  # Disallowed when conditions are present
                conditions=["trade_in_500_required"]
            )

if __name__ == "__main__":
    unittest.main()
