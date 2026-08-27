#!/usr/bin/env python3
"""Test suite for Ticket 22: Build official domestic and global source-routing playbooks.
Tests:
1. Pass: Routes HDR claim to VESA DisplayHDR registry with runtime search syntax and proof boundaries.
2. Pass: Routes standard status to std.samr.gov.cn with what it proves vs cannot prove alone.
3. Pass: Routes FCC internal teardown to FCC OET Equipment Authorization database.
4. Adversarial: Missing USB-IF voluntary listing is classified as unverified_voluntary_listing, NOT noncompliant.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_routing_playbooks import (
    route_claim_to_source_playbook,
    handle_voluntary_registry_absence,
    SOURCE_ROUTING_PLAYBOOKS
)

class TestTicket22SourceRouting(unittest.TestCase):
    def test_01_vesa_hdr_routing_and_proof_limits(self):
        """Pass path: HDR claims route to VESA DisplayHDR with exact search syntax."""
        res = route_claim_to_source_playbook(claim_type="DisplayHDR_1000", query_variable="Monitor Alpha Pro")
        self.assertEqual(res["source_id"], "VESA_DISPLAYHDR")
        self.assertIn("displayhdr.org", res["portal_url"])
        self.assertIn("Monitor Alpha Pro", res["runtime_search_syntax"])
        self.assertIn("True certified HDR peak luminance", res["what_it_proves"])
        self.assertIn("cannot_prove_alone", res)

    def test_02_samr_standard_routing(self):
        """Pass path: GB 4806 standard routes to std.samr.gov.cn."""
        res = route_claim_to_source_playbook(claim_type="food_contact_standard", query_variable="GB 4806.1-2016")
        self.assertEqual(res["source_id"], "CN_SAMR_STANDARDS")
        self.assertIn("std.samr.gov.cn", res["portal_url"])
        self.assertIn("active, upcoming, or superseded", res["what_it_proves"])

    def test_03_fcc_teardown_routing(self):
        """Pass path: RF and internal PCB teardown photos route to FCC database."""
        res = route_claim_to_source_playbook(claim_type="fcc_internal_photos", query_variable="2BC34-XYZ")
        self.assertEqual(res["source_id"], "US_FCC_ID")
        self.assertIn("fcc.gov", res["portal_url"])

    def test_04_adversarial_usb_if_absence_not_noncompliant(self):
        """Adversarial path: Absence in voluntary USB-IF list cannot be converted into 'noncompliant' or fake."""
        res = handle_voluntary_registry_absence(
            registry_name="USB-IF",
            query_item="GaN Fast Cable Type-C",
            found_in_registry=False
        )
        self.assertEqual(res["status"], "unverified_voluntary_listing")
        self.assertFalse(res["is_noncompliant"])
        self.assertIn("does not imply physical noncompliance", res["notes"])

if __name__ == "__main__":
    unittest.main()
