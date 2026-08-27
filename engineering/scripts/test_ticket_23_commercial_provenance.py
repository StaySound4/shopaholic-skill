#!/usr/bin/env python3
"""Test suite for Ticket 23: Record commercial relationships, sample provenance, and source conflicts.
Tests:
1. Pass: Manufacturer loaner review supports observed measurement with disclosed caveat if methodology transparent.
2. Pass: Sponsored ad copy cannot alone establish comparative durability over competitors.
3. Pass: Multi-source discrepancy triggers explicit conflict_disputed state and adopts independent retail data.
4. Adversarial: Affiliate commission flag alone must NOT erase an independently reproducible measured fact.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commercial_provenance_engine import adjudicate_evidence_with_commercial_context

class TestTicket23CommercialProvenance(unittest.TestCase):
    def test_01_transparent_sponsored_measurement_admissible(self):
        """Pass path: Manufacturer loaner with transparent test method is accepted with bias disclosure."""
        source = {
            "commercial_relationships": ["loaner"],
            "sample_provenance": "manufacturer_supplied",
            "is_methodology_transparent": True
        }
        res = adjudicate_evidence_with_commercial_context(
            claim_target="objective_measurement",
            claimed_value=850.0,
            evidence_source=source
        )
        self.assertTrue(res["admissible"])
        self.assertEqual(res["status"], "verified_with_commercial_caveat")
        self.assertIn("commercial tags", res["bias_disclosure"])

    def test_02_sponsored_source_cannot_prove_comparative_superiority_alone(self):
        """Pass path: Sponsored source alone cannot establish comparative durability over rivals."""
        source = {
            "commercial_relationships": ["sponsored", "advertising"],
            "sample_provenance": "loaner",
            "is_methodology_transparent": False
        }
        res = adjudicate_evidence_with_commercial_context(
            claim_target="comparative_durability",
            claimed_value="2x more durable than competitor X",
            evidence_source=source,
            corroborating_independent_sources=[]
        )
        self.assertFalse(res["admissible"])
        self.assertEqual(res["confidence"], "U")
        self.assertEqual(res["status"], "rejected_unsubstantiated_commercial_claim")

    def test_03_multi_source_conflict_explicitly_preserved(self):
        """Pass path: Commercial claim conflicting with independent retail sample triggers conflict_disputed."""
        commercial_source = {
            "commercial_relationships": ["brand_owned"],
            "sample_provenance": "manufacturer_supplied",
            "is_methodology_transparent": True
        }
        independent_source = {
            "commercial_relationships": ["unknown"],
            "sample_provenance": "self_purchased",
            "measured_value": 720.0
        }
        res = adjudicate_evidence_with_commercial_context(
            claim_target="objective_measurement",
            claimed_value=1000.0,
            evidence_source=commercial_source,
            corroborating_independent_sources=[independent_source]
        )
        self.assertEqual(res["status"], "conflict_disputed")
        self.assertEqual(res["value_adopted"], 720.0)
        self.assertIn("Multi-source conflict", res["bias_disclosure"])

    def test_04_adversarial_affiliate_flag_cannot_erase_reproducible_fact(self):
        """Adversarial path: Affiliate flag must NOT erase an independently reproducible measured fact."""
        affiliate_source = {
            "commercial_relationships": ["affiliate"],
            "sample_provenance": "self_purchased",
            "is_methodology_transparent": True
        }
        res = adjudicate_evidence_with_commercial_context(
            claim_target="objective_measurement",
            claimed_value="100% sRGB / 95% DCI-P3",
            evidence_source=affiliate_source
        )
        # Must strictly be admissible and NOT discarded
        self.assertTrue(res["admissible"])
        self.assertEqual(res["value_adopted"], "100% sRGB / 95% DCI-P3")
        self.assertNotEqual(res["confidence"], "U")

if __name__ == "__main__":
    unittest.main()
