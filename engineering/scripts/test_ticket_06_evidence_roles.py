#!/usr/bin/env python3
"""Test suite for Ticket 06: Replace universal L1-L4 truth ranking with claim-specific evidence roles.
Tests both happy path and adversarial conditions:
1. Seller offer (market_price) appropriately supports price.
2. Official manual (official_primary) appropriately supports declared dimensions/interfaces.
3. VESA registry (voluntary_certification) appropriately supports DisplayHDR tier.
4. Independent lab (independent_measurement) appropriately supports measured performance.
5. Official spec cannot alone prove comparative superiority over competitors.
6. Adversarial path: Ten seller pages asserting durability cannot upgrade a high-impact claim to verified.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_role_router import is_source_role_appropriate, evaluate_evidence_packet_for_claim

class TestTicket06EvidenceRoles(unittest.TestCase):
    def test_01_claim_specific_role_appropriateness(self):
        """Pass path: Appropriate sources correctly support matching claim types."""
        # 1. Price from market_price
        self.assertTrue(is_source_role_appropriate("market_price", "price_and_availability"))
        
        # 2. Dimensions from official_primary
        self.assertTrue(is_source_role_appropriate("official_primary", "declared_dimension_interface"))
        
        # 3. Voluntary certification tier from voluntary_certification
        self.assertTrue(is_source_role_appropriate("voluntary_certification", "voluntary_technical_tier"))
        
        # 4. Measured performance from independent_measurement
        self.assertTrue(is_source_role_appropriate("independent_measurement", "measured_performance"))
        
        # 5. Safety certification from regulatory
        self.assertTrue(is_source_role_appropriate("regulatory", "safety_certification"))

    def test_02_official_spec_cannot_prove_comparative_superiority(self):
        """Pass path: Official spec supports features/dimensions but cannot prove comparative superiority."""
        self.assertTrue(is_source_role_appropriate("official_primary", "declared_dimension_interface"))
        self.assertFalse(is_source_role_appropriate("official_primary", "comparative_superiority"))
        
        packet = [{"source_id": "SRC-OFFICIAL", "source_role": "official_primary"}]
        res = evaluate_evidence_packet_for_claim("comparative_superiority", packet)
        self.assertFalse(res["overall_appropriate"])
        self.assertFalse(res["can_verify"])

    def test_03_adversarial_ten_seller_pages_cannot_prove_durability(self):
        """Adversarial path: 10 seller marketing pages claiming durability cannot verify a high-impact durability claim."""
        ten_seller_sources = [
            {"source_id": f"SRC-SELLER-{i}", "source_role": "market_price", "publisher": f"Store {i}"}
            for i in range(1, 11)
        ]
        
        # Attempt to verify long_term_durability claim using only market_price sources
        res = evaluate_evidence_packet_for_claim("long_term_durability", ten_seller_sources)
        
        # Must strictly fail verification regardless of count
        self.assertEqual(res["total_source_count"], 10)
        self.assertEqual(res["appropriate_source_count"], 0)
        self.assertFalse(res["overall_appropriate"])
        self.assertFalse(res["can_verify"])
        self.assertTrue(any("No source has an appropriate role" in r for r in res["reasons"]))

if __name__ == "__main__":
    unittest.main()
