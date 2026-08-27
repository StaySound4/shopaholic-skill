#!/usr/bin/env python3
"""Test suite for Ticket 09: Add provenance and corporate-role graph.
Tests both happy path and adversarial conditions:
1. Distinct corporate roles (Brand owner, Regulatory applicant, Manufacturer, Seller) preserved independently.
2. Proprietary OEM manufacturing (e.g. Apple/Foxconn) classified as proprietary_oem without negative rebadge stigma.
3. Public-tooling rebadging unmasked with markup calculation (>=30%~40% threshold flag).
4. Gray market, export-return, and bulk-pack channel risks explicitly identified.
5. Adversarial path: Marketplace 'brand story' cannot overwrite regulatory manufacturer records.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance_graph import build_provenance_graph, handle_entity_conflict

class TestTicket09Provenance(unittest.TestCase):
    def test_01_distinct_roles_preserved(self):
        """Pass path: Four distinct entities preserve all roles with respective evidence."""
        role_assignments = {
            "brand_owner": {"name": "DJI Innovations", "jurisdiction": "CN", "evidence_source_ref": "https://trademark.gov.cn/123"},
            "regulatory_applicant": {"name": "Shenzhen Dajiang Baiwang Technology", "jurisdiction": "CN", "evidence_source_ref": "3C Cert #20260109"},
            "manufacturer": {"name": "Dongguan Precision Manufacturing Co.", "jurisdiction": "CN", "evidence_source_ref": "3C Factory #A01"},
            "seller": {"name": "DJI Official Flagship Store (JD.com)", "jurisdiction": "CN", "evidence_source_ref": "JD Storefront #987"}
        }
        
        graph = build_provenance_graph(role_assignments, upstream_odm_oem=None, is_proprietary_tooling=True)
        
        roles = graph["roles"]
        self.assertEqual(roles["brand_owner"]["entity_name"], "DJI Innovations")
        self.assertEqual(roles["regulatory_applicant"]["entity_name"], "Shenzhen Dajiang Baiwang Technology")
        self.assertEqual(roles["manufacturer"]["entity_name"], "Dongguan Precision Manufacturing Co.")
        self.assertEqual(roles["seller"]["entity_name"], "DJI Official Flagship Store (JD.com)")
        self.assertIsNone(roles["importer"]) # Unknown remains None

    def test_02_proprietary_oem_vs_public_tooling_rebadge(self):
        """Pass path: Proprietary custom OEM is separated from public-tooling rebadging."""
        # 1. Proprietary custom OEM
        graph_oem = build_provenance_graph(
            role_assignments={"brand_owner": {"name": "Apple Inc."}},
            upstream_odm_oem="Hon Hai / Foxconn",
            is_proprietary_tooling=True
        )
        self.assertEqual(graph_oem["rebadging_type"], "proprietary_oem")
        self.assertIsNone(graph_oem["rebadge_unmasked"])
        
        # 2. Public tooling rebadge with 80% markup over upstream OEM
        graph_rebadge = build_provenance_graph(
            role_assignments={"brand_owner": {"name": "Trendy White-Label Brand"}},
            upstream_odm_oem="Cixi Generic Appliance OEM",
            upstream_base_price=50.0,
            current_retail_price=90.0,
            is_proprietary_tooling=False
        )
        self.assertEqual(graph_rebadge["rebadging_type"], "public_tooling_rebadge")
        self.assertIsNotNone(graph_rebadge["rebadge_unmasked"])
        self.assertEqual(graph_rebadge["rebadge_unmasked"]["estimated_markup_percentage"], 80.0)
        self.assertTrue(graph_rebadge["rebadge_unmasked"]["excessive_markup_flag"])

    def test_03_gray_market_channel_risks(self):
        """Pass path: Export-return and parallel-import channel risks are explicitly labeled."""
        graph_parallel = build_provenance_graph({}, channel_type="parallel_import")
        self.assertTrue(any("parallel_import_gray_market" in r for r in graph_parallel["channel_risks"]))
        
        graph_export = build_provenance_graph({}, channel_type="export_return")
        self.assertTrue(any("export_return" in r for r in graph_export["channel_risks"]))

    def test_04_adversarial_marketplace_story_cannot_overwrite_regulatory_records(self):
        """Adversarial path: Marketplace promotional claims of 'German Craftsmanship' cannot overwrite domestic regulatory manufacturer record."""
        conflict = handle_entity_conflict(
            regulatory_manufacturer="Zhejiang OEM Factory Co., Ltd.",
            marketing_story_brand="Munich Artisan Heritage Gmbh",
            evidence_regulatory="SAMR 3C Database #20260109",
            evidence_marketing="Store Product Detail Page Hero Banner"
        )
        
        self.assertTrue(conflict["conflict_detected"])
        self.assertEqual(conflict["resolved_manufacturer"], "Zhejiang OEM Factory Co., Ltd.")
        self.assertEqual(conflict["status"], "regulatory_authority_preserved")

if __name__ == "__main__":
    unittest.main()
