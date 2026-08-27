#!/usr/bin/env python3
"""Test suite for Ticket 28: Replace 'high-position anti-sycophancy' with truth-first correction protocol.
Tests:
1. Pass: Verified new model spec corrects stale assumption, propagates to ledger, and ranking recomputes.
2. Adversarial: Unsupported or refuted user assertion is strictly NOT accepted merely to agree (no sycophancy).
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from truth_correction_protocol import evaluate_user_correction

class TestTicket28TruthCorrection(unittest.TestCase):
    def test_01_verified_correction_acknowledged_and_propagated(self):
        """Pass path: Verified user correction updates ledger and recomputes candidates."""
        evidence = {
            "is_authoritative": True,
            "source_id": "OFFICIAL_PRODUCT_MANUAL_REV_B",
            "verified_value": "USB-C"
        }
        candidates = [
            {"name": "Camera Alpha", "port_type": "Micro-USB", "score": 85.0}
        ]
        
        res = evaluate_user_correction(
            user_claim_field="port_type",
            user_claimed_value="USB-C",
            prior_system_value="Micro-USB",
            verification_evidence=evidence,
            current_candidates=candidates
        )
        
        self.assertTrue(res["correction_accepted"])
        self.assertEqual(res["adopted_value"], "USB-C")
        self.assertEqual(res["recomputed_ranking"][0]["port_type"], "USB-C")
        self.assertIn("修正确认", res["acknowledgement_message"])
        self.assertTrue(res["sycophancy_avoided"])

    def test_02_adversarial_unsupported_user_assertion_rejected(self):
        """Adversarial path: Unsupported or refuted user assertion is not accepted to please user."""
        refuting_evidence = {
            "is_authoritative": True,
            "source_id": "CN_3C_CERTIFICATE",
            "verified_value": 2500.0  # Official certified limit is 2500W
        }
        
        res = evaluate_user_correction(
            user_claim_field="max_power_wattage",
            user_claimed_value=5000.0, # User claims 5000W
            prior_system_value=2500.0,
            verification_evidence=refuting_evidence
        )
        
        # Must strictly refuse to accept false user assertion
        self.assertFalse(res["correction_accepted"])
        self.assertEqual(res["adopted_value"], 2500.0)
        self.assertIn("未获证实", res["acknowledgement_message"])
        self.assertIn("Refuted by authoritative source", res["evidence_notes"])
        self.assertTrue(res["sycophancy_avoided"])

if __name__ == "__main__":
    unittest.main()
