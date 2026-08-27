#!/usr/bin/env python3
"""Test suite for Ticket 05: Introduce claim/evidence ledger with explicit unknown and conflict states.
Tests both happy path and adversarial conditions:
1. High-impact claim validation with status adjudication (verified, disputed, unverified).
2. Official 500g vs Independent 535g yields a structured Claim-Metric Discrepancy (CMD) and disputed status.
3. Precise scoping to product, region SKU, revision, and batch.
4. Preserving contradicting sources and missing evidence honesty.
5. Adversarial path: A new-product long-term durability claim with no evidence MUST remain unverified (grade U).
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from claim_ledger import create_claim_record, validate_claim_ledger_entry

class TestTicket05ClaimLedger(unittest.TestCase):
    def test_01_disputed_weight_claim_with_cmd(self):
        """Pass path: Official 500g vs independent 535g yields a disputed weight claim with structured CMD."""
        claim = create_claim_record(
            claim_id="CLM-WEIGHT-001",
            claim="Product bare body weight is 500g",
            claim_type="weight_specification",
            impact="medium",
            entity_id="PROD-CAMERA-X",
            region_sku="CN",
            supporting_sources=["https://official-brand.com/specs/500g"],
            contradicting_sources=["https://independent-lab.org/review/measured-535g"],
            claimed_value="500g",
            claimed_source_ref="Official Spec Sheet",
            measured_value="535g",
            measured_source_ref="Independent Lab Calibrated Scale",
            deviation_type="laboratory_vs_realworld",
            severity="minor"
        )
        
        errors = validate_claim_ledger_entry(claim)
        self.assertEqual(errors, [])
        self.assertEqual(claim["status"], "disputed")
        self.assertEqual(claim["evidence_grade"], "B")
        self.assertIsNotNone(claim["discrepancy"])
        self.assertEqual(claim["discrepancy"]["claimed_value"], "500g")
        self.assertEqual(claim["discrepancy"]["measured_value"], "535g")
        self.assertEqual(claim["discrepancy"]["deviation_type"], "laboratory_vs_realworld")

    def test_02_scoped_claim_to_revision_and_batch(self):
        """Pass path: Claims are strictly scoped to revision and batch."""
        claim = create_claim_record(
            claim_id="CLM-CAPACITOR-002",
            claim="Uses 105C Japanese capacitors",
            claim_type="component_sourcing",
            impact="high",
            entity_id="PROD-PSU-750W",
            revision="Rev 1.0",
            batch="Batch 2026-Q1",
            supporting_sources=["https://teardown.net/psu750/rev1.0"],
            source_role_appropriate=True
        )
        
        errors = validate_claim_ledger_entry(claim)
        self.assertEqual(errors, [])
        self.assertEqual(claim["scope"]["revision"], "Rev 1.0")
        self.assertEqual(claim["scope"]["batch"], "Batch 2026-Q1")
        self.assertEqual(claim["status"], "verified")
        self.assertEqual(claim["evidence_grade"], "S")

    def test_03_adversarial_new_product_unverified_durability_claim(self):
        """Adversarial path: A brand claiming '10-year maintenance free durability' on a brand-new release must remain unverified."""
        unverified_claim = create_claim_record(
            claim_id="CLM-DURABILITY-003",
            claim="Guaranteed 10-year maintenance-free operational durability under extreme dust",
            claim_type="long_term_durability",
            impact="critical",
            entity_id="PROD-VACUUM-NEW",
            supporting_sources=[], # No long term historical data exists for new launch
            contradicting_sources=[]
        )
        
        errors = validate_claim_ledger_entry(unverified_claim)
        self.assertEqual(errors, [])
        self.assertEqual(unverified_claim["status"], "unverified")
        self.assertEqual(unverified_claim["evidence_grade"], "U")
        
        # Adversarial check: Forcing status to 'verified' without supporting sources must trigger validation failure
        tampered_claim = dict(unverified_claim)
        tampered_claim["status"] = "verified"
        tampered_errors = validate_claim_ledger_entry(tampered_claim)
        self.assertGreater(len(tampered_errors), 0)
        self.assertTrue(any("No supporting sources" in e for e in tampered_errors))

if __name__ == "__main__":
    unittest.main()
