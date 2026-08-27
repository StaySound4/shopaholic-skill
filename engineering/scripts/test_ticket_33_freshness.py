#!/usr/bin/env python3
"""Test suite for Ticket 33: Add freshness guards for static references and runtime temporal facts.
Tests:
1. Pass: Dynamic year resolution for tokens and fixed year literals (2025/2026), active standard status (GB 4706.1-2024), and standard errata (IEEE 1789 vs 1788).
2. Pass: Superseded and repealed standard statuses detected.
3. Pass: Timeless physical principles remain undated and valid.
4. Adversarial: Stale static reference cannot override live registry active status from std.samr.gov.cn; expired references degrade to B.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from freshness_guard_engine import (
    resolve_dynamic_query_year,
    audit_standard_citation,
    evaluate_reference_freshness
)

class TestTicket33Freshness(unittest.TestCase):
    def test_01_dynamic_year_literal_and_standard_errata_resolution(self):
        """Pass path: Dynamic year token AND fixed year literals (2025/2026) resolved, IEEE 1788 erratum detected, GB 4706.1-2024 verified active."""
        # 1. Dynamic year for placeholder and 2025/2026 literals
        query_token = resolve_dynamic_query_year("best OLED monitor {{CURRENT_YEAR}} deals", current_year=2027)
        self.assertEqual(query_token, "best OLED monitor 2027 deals")

        query_literal_2025 = resolve_dynamic_query_year("best coffee grinder 2025 recommendations", current_year=2027)
        self.assertEqual(query_literal_2025, "best coffee grinder 2027 recommendations")

        query_literal_2026 = resolve_dynamic_query_year("best display monitors 2026 guide", current_year=2027)
        self.assertEqual(query_literal_2026, "best display monitors 2027 guide")

        # 2. IEEE 1788 vs 1789 erratum
        erratum_res = audit_standard_citation("This lamp complies with IEEE 1788-2015 low flicker standard.", "IEEE 1789-2015")
        self.assertFalse(erratum_res["is_valid"])
        self.assertEqual(erratum_res["error_type"], "standard_code_erratum")
        self.assertIn("IEEE 1789-2015", erratum_res["correction"])

        # 3. GB 4706.1-2024 active status
        status_res = audit_standard_citation("GB 4706.1-2024 is an upcoming draft standard for safety.", "GB 4706.1-2024")
        self.assertFalse(status_res["is_valid"])
        self.assertEqual(status_res["error_type"], "obsolete_status_phrasing")
        self.assertEqual(status_res["status"], "active")

    def test_02_superseded_and_repealed_standard_audit(self):
        """Pass path: Superseded standard (GB 4706.1-2005) and repealed status are flagged."""
        res_superseded = audit_standard_citation("Complies with GB 4706.1-2005 appliance standard.", "GB 4706.1-2005")
        self.assertFalse(res_superseded["is_valid"])
        self.assertEqual(res_superseded["status"], "superseded")
        self.assertEqual(res_superseded["successor"], "GB 4706.1-2024")

        res_repealed = audit_standard_citation("Complies with old standard", "OLD_STD", live_registry_status="repealed")
        self.assertFalse(res_repealed["is_valid"])
        self.assertEqual(res_repealed["status"], "repealed")

    def test_03_timeless_physical_principles_undated(self):
        """Pass path: Stable physical/optical/acoustic principles remain undated without expiry."""
        res = evaluate_reference_freshness(
            reference_id="BEER_LAMBERT_LAW_OPTICS",
            published_date_str="1990-01-01",
            is_timeless_physics=True
        )
        self.assertTrue(res["is_fresh"])
        self.assertEqual(res["confidence_grade"], "S")
        self.assertFalse(res.get("requires_reverification", False))

    def test_04_adversarial_stale_reference_overridden_and_degraded(self):
        """Adversarial path: Stale cached text cannot override live registry, and old price references degrade to B."""
        # Live registry check overrides stale text
        res = audit_standard_citation(
            citation_text="GB 4706.1-2024 is upcoming",
            target_standard_code="GB 4706.1-2024",
            live_registry_status="active"
        )
        self.assertEqual(res["status"], "active")
        self.assertFalse(res["is_valid"])

        # Stale pricing reference (300 days old)
        price_freshness = evaluate_reference_freshness(
            reference_id="JD_HISTORICAL_PRICE_SNAP",
            published_date_str="2025-10-01",
            is_timeless_physics=False,
            current_date_str="2026-08-28",
            ttl_days=180
        )
        self.assertFalse(price_freshness["is_fresh"])
        self.assertEqual(price_freshness["confidence_grade"], "B")
        self.assertTrue(price_freshness["requires_reverification"])

if __name__ == "__main__":
    unittest.main()
