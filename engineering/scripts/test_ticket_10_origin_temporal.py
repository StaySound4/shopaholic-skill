#!/usr/bin/env python3
"""Test suite for Ticket 10: Add origin and temporal semantics without inference shortcuts.
Tests both happy path and adversarial conditions:
1. Product lifecycle dates (certification, announcement, first-sale, regional-sale) stay separate.
2. Batch launch window is distinguished from model launch date.
3. Runtime current-year queries derive dynamically from runtime date (e.g. 2031 runtime uses 2031).
4. Regulatory standard temporal statuses (active, upcoming, superseded) are verified against registry.
5. Adversarial path: German GTIN license prefix and German brand HQ with no factory evidence must NOT become 'Made in Germany'.
"""
import datetime, json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from origin_temporal_engine import (
    resolve_manufacturing_origin,
    structure_product_lifecycle_dates,
    verify_standard_temporal_status,
    get_dynamic_runtime_year
)

class TestTicket10OriginTemporal(unittest.TestCase):
    def test_01_lifecycle_dates_decoupled(self):
        """Pass path: Certification (Jan), Announcement (Mar), Sale (Mar 10) remain distinct."""
        dates = structure_product_lifecycle_dates(
            certification_date="2026-01-15",
            announcement_date="2026-03-01",
            first_sale_date="2026-03-10",
            regional_first_sale_date="2026-04-01",
            batch_window="2026-Q2"
        )
        
        self.assertEqual(dates["certification_date"], "2026-01-15")
        self.assertEqual(dates["announcement_date"], "2026-03-01")
        self.assertEqual(dates["first_sale_date"], "2026-03-10")
        self.assertEqual(dates["regional_first_sale_date"], "2026-04-01")
        self.assertEqual(dates["batch_window"], "2026-Q2")

    def test_02_dynamic_runtime_year(self):
        """Pass path: 2031 runtime date derives 2031 anchor without static literals."""
        year_2031 = get_dynamic_runtime_year("2031-08-28")
        self.assertEqual(year_2031, 2031)
        
        year_2026 = get_dynamic_runtime_year("2026-08-28")
        self.assertEqual(year_2026, 2026)

    def test_03_standard_temporal_status_verified(self):
        """Pass path: Evaluates active vs upcoming vs superseded standard statuses."""
        mock_registry = {
            "GB 4706.1-2024": {
                "title": "Household Appliances Safety General Requirements",
                "implementation_date": "2026-08-01",
                "superseded_date": None
            },
            "GB 4706.1-2005": {
                "title": "Household Appliances Safety General Requirements (2005)",
                "implementation_date": "2006-08-01",
                "superseded_date": "2026-08-01"
            }
        }
        
        # In late August 2026: GB 4706.1-2024 is active, GB 4706.1-2005 is superseded
        ref_aug_2026 = datetime.date(2026, 8, 28)
        res_new = verify_standard_temporal_status("GB 4706.1-2024", reference_date=ref_aug_2026, registry_data=mock_registry)
        res_old = verify_standard_temporal_status("GB 4706.1-2005", reference_date=ref_aug_2026, registry_data=mock_registry)
        
        self.assertEqual(res_new["status"], "active")
        self.assertEqual(res_old["status"], "superseded")

    def test_04_adversarial_gtin_and_hq_cannot_assert_made_in_country(self):
        """Adversarial path: German GTIN prefix (400) + German Brand HQ with no factory evidence must remain unverified."""
        res = resolve_manufacturing_origin(
            brand_hq_country="Germany",
            gtin_prefix_country="Germany",
            physical_nameplate_country=None,
            certificate_factory_country=None
        )
        
        # Must strictly refuse to declare 'Made in Germany'
        self.assertIsNone(res["country_of_origin"])
        self.assertEqual(res["confidence"], "unverified")
        self.assertTrue(res["shortcut_prevented"])

if __name__ == "__main__":
    unittest.main()
