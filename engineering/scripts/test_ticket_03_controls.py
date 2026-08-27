#!/usr/bin/env python3
"""Test suite for Ticket 03: Add evaluator positive and sham controls.
Tests both happy path and adversarial conditions:
1. Positive control (C_positive_bad_evidence) worsens evidence/appropriateness metrics.
2. Sham control (C_sham_style) does not gain correctness/evidence metrics merely from style.
3. Evaluator control check validates protocol before interpreting runs.
4. Adversarial path: Presentation-biased scoring is caught and invalidates confirmatory interpretation.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from control_evaluator import score_evidence_appropriateness, verify_control_validity

class TestTicket03Controls(unittest.TestCase):
    def test_01_positive_control_worsens_evidence_metrics(self):
        """Pass path: Deliberate bad-evidence mutations produce degraded scores."""
        baseline_record = {
            "condition": "B1_uploaded_current",
            "claims": [
                {"source_role": "independent_lab", "claim_type": "lab_measurement", "evidence_tier": "S"},
                {"source_role": "regulatory_registry", "claim_type": "safety_certification", "evidence_tier": "S"}
            ]
        }
        positive_control_record = {
            "condition": "C_positive_bad_evidence",
            "claims": [
                {"source_role": "seller_marketing", "claim_type": "lab_measurement", "evidence_tier": "U"},
                {"source_role": "promotional", "claim_type": "safety_certification", "evidence_tier": "U"}
            ]
        }
        
        base_metrics = score_evidence_appropriateness(baseline_record)
        pos_metrics = score_evidence_appropriateness(positive_control_record)
        
        self.assertGreater(base_metrics["source_role_appropriateness"], pos_metrics["source_role_appropriateness"])
        self.assertGreater(pos_metrics["unsupported_claim_rate"], base_metrics["unsupported_claim_rate"])

    def test_02_sham_control_does_not_gain_correctness(self):
        """Pass path: Styling changes alone do not improve evidence or constraint metrics."""
        baseline_record = {
            "condition": "B1_uploaded_current",
            "raw_text": "Product A satisfies standard 3C.",
            "claims": [{"source_role": "regulatory_registry", "claim_type": "safety_certification", "evidence_tier": "S"}]
        }
        sham_record = {
            "condition": "C_sham_style",
            "raw_text": "🌟✨ **SUPER RECOMMENDATION** ✨🌟\n| Product | Rating | Features |\n|---|---|---|\n| Product A | 💯 | Satisfies standard 3C |",
            "claims": [{"source_role": "regulatory_registry", "claim_type": "safety_certification", "evidence_tier": "S"}]
        }
        
        base_metrics = score_evidence_appropriateness(baseline_record)
        sham_metrics = score_evidence_appropriateness(sham_record)
        
        # Sham style should have identical evidence correctness
        self.assertEqual(base_metrics["source_role_appropriateness"], sham_metrics["source_role_appropriateness"])
        self.assertEqual(base_metrics["hard_constraint_compliance"], sham_metrics["hard_constraint_compliance"])

    def test_03_control_validity_pass(self):
        """Pass path: When positive control degrades and sham control does not gain, evaluator validity passes."""
        base_metrics = {"source_role_appropriateness": 0.90, "unsupported_claim_rate": 0.10}
        pos_metrics = {"source_role_appropriateness": 0.20, "unsupported_claim_rate": 0.80}
        sham_metrics = {"source_role_appropriateness": 0.90, "unsupported_claim_rate": 0.10}
        
        res = verify_control_validity(base_metrics, pos_metrics, sham_metrics)
        self.assertTrue(res["valid"])
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(len(res["reasons"]), 0)

    def test_04_adversarial_presentation_biased_evaluator_is_invalidated(self):
        """Adversarial path: An evaluator biased toward verbose/styled presentation fails the sham check and is invalidated."""
        baseline_record = {
            "condition": "B1_uploaded_current",
            "raw_text": "Short decision." # ~15 chars
        }
        sham_record = {
            "condition": "C_sham_style",
            "raw_text": "🌟 Very long and beautifully formatted report with multiple huge tables and decorative headers... " * 10 # ~900 chars
        }
        pos_record = {
            "condition": "C_positive_bad_evidence",
            "raw_text": "Decent length output with fake claims... " * 10
        }
        
        # Evaluate using presentation-biased rubric
        base_metrics = score_evidence_appropriateness(baseline_record, rubric_type="presentation_biased")
        pos_metrics = score_evidence_appropriateness(pos_record, rubric_type="presentation_biased")
        sham_metrics = score_evidence_appropriateness(sham_record, rubric_type="presentation_biased")
        
        # Sham gained score purely from length/style
        self.assertGreater(sham_metrics["source_role_appropriateness"], base_metrics["source_role_appropriateness"])
        
        # Verifier must detect this invalid presentation bias
        res = verify_control_validity(base_metrics, pos_metrics, sham_metrics)
        self.assertFalse(res["valid"])
        self.assertEqual(res["status"], "INVALID_EVALUATOR")
        self.assertTrue(any("SHAM_CONTROL_FAILURE" in r for r in res["reasons"]))

if __name__ == "__main__":
    unittest.main()
