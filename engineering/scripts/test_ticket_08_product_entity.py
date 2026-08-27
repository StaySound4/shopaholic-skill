#!/usr/bin/env python3
"""Test suite for Ticket 08: Resolve Canonical Product, Region SKU, Revision, and Batch.
Tests both happy path and adversarial conditions:
1. Bundle/accessory SKUs resolve to one host canonical product.
2. Distinct Region SKUs (CN 220V 3C vs US 120V FCC ID/UL) remain isolated with jurisdiction compliance IDs.
3. Batch identification provides manufacturing window and physical SN/nameplate verification method.
4. Adversarial path: A hardware revision with modified/removed interfaces CANNOT inherit old revision claims.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from product_entity_resolver import (
    resolve_product_entity,
    match_bundle_to_canonical,
    check_feature_inheritance_across_revisions
)

class TestTicket08ProductEntity(unittest.TestCase):
    def test_01_bundle_to_canonical_mapping(self):
        """Pass path: Different retail bundle SKUs resolve to the same canonical host product."""
        known_canonical = [
            {"brand": "Sony", "model_name": "A7M4", "model_code": "ILCE-7M4"}
        ]
        
        bundle_1 = "Sony A7M4 Body Only Kit (Official CN)"
        bundle_2 = "Sony A7M4 with 28-70mm Zoom Lens Bundle"
        
        match_1 = match_bundle_to_canonical(bundle_1, known_canonical)
        match_2 = match_bundle_to_canonical(bundle_2, known_canonical)
        
        self.assertIsNotNone(match_1)
        self.assertIsNotNone(match_2)
        self.assertEqual(match_1["model_code"], "ILCE-7M4")
        self.assertEqual(match_2["model_code"], "ILCE-7M4")

    def test_02_region_sku_jurisdiction_isolation(self):
        """Pass path: CN (220V, 3C) and US (120V, FCC/UL) variants are strictly isolated."""
        entity_cn = resolve_product_entity(
            brand="Anker",
            model_name="Prime 100W Charger",
            region_sku="CN",
            region="China",
            identifiers={"3c_cert": "2026010907123456", "voltage": "220V"},
            certifications=[{"standard_or_cert_name": "GB 4943.1-2022", "jurisdiction": "china", "status": "active"}]
        )
        
        entity_us = resolve_product_entity(
            brand="Anker",
            model_name="Prime 100W Charger",
            region_sku="US",
            region="North America",
            identifiers={"fcc_id": "2AB7K-A2343", "ul_id": "E123456", "voltage": "120V"},
            certifications=[{"standard_or_cert_name": "UL 62368-1", "jurisdiction": "north_america", "status": "active"}]
        )
        
        # Entity IDs and jurisdiction compliance IDs must be strictly distinct
        self.assertNotEqual(entity_cn["entity_id"], entity_us["entity_id"])
        self.assertEqual(entity_cn["region_sku"], "CN")
        self.assertEqual(entity_us["region_sku"], "US")
        self.assertIn("3c_cert", entity_cn["identifiers"])
        self.assertIn("fcc_id", entity_us["identifiers"])
        self.assertEqual(entity_cn["identifiers"]["voltage"], "220V")
        self.assertEqual(entity_us["identifiers"]["voltage"], "120V")

    def test_03_batch_and_physical_verification_rule(self):
        """Pass path: Batch representation includes launch window and physical SN/nameplate verification method."""
        entity_batch = resolve_product_entity(
            brand="Seasonic",
            model_name="Focus GX-850",
            region_sku="CN",
            revision="Rev 1.2",
            batch="2026-Q1",
            dates={"batch_window": "2026-01 to 2026-03"},
            physical_verification_rule="Inspect physical power supply label: check 4th-8th digit of serial number for '2601' or '2602' batch code."
        )
        
        self.assertEqual(entity_batch["batch"], "2026-Q1")
        self.assertEqual(entity_batch["dates"]["batch_window"], "2026-01 to 2026-03")
        self.assertIn("serial number", entity_batch["physical_verification_rule"])

    def test_04_adversarial_hardware_revision_cannot_inherit_obsolete_claims(self):
        """Adversarial path: Rev 2.0 with changed controller/ports CANNOT inherit Rev 1.0 feature claims."""
        changelog = {
            "source_revision": "Rev 1.0",
            "target_revision": "Rev 2.0",
            "removed_features": ["DisplayPort 1.4 port", "RGB ambient lighting"],
            "changed_components": ["Swapped Phison E18 controller to Innogrit IG5236"]
        }
        
        claim_dp = "Features dedicated DisplayPort 1.4 output"
        claim_controller = "Equipped with Phison E18 flagship controller"
        
        # Checking inheritance
        can_inherit_dp = check_feature_inheritance_across_revisions(
            claim_text=claim_dp,
            source_revision="Rev 1.0",
            target_revision="Rev 2.0",
            revision_changelog=changelog
        )
        can_inherit_controller = check_feature_inheritance_across_revisions(
            claim_text=claim_controller,
            source_revision="Rev 1.0",
            target_revision="Rev 2.0",
            revision_changelog=changelog
        )
        
        # Both must be rejected
        self.assertFalse(can_inherit_dp)
        self.assertFalse(can_inherit_controller)

if __name__ == "__main__":
    unittest.main()
