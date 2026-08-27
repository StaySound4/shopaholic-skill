#!/usr/bin/env python3
"""Test suite for Ticket 40: Publish the v1.0 evidence dossier and only then claim measured improvement.
Tests:
1. Pass: Complete dossier with all permanent stamps and traceable claims validates cleanly.
2. Pass: Disclosed limitations, blocked rates, and failure rates are present.
3. Adversarial: Removing raw-run linkage downgrades claim status to DOWNGRADED_UNVERIFIABLE.
4. Adversarial: README with improvement claims before gate clearance is flagged.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_dossier_generator import (
    generate_evidence_dossier,
    validate_dossier_claim_traceability,
    validate_readme_wording_compliance
)

class TestTicket40EvidenceDossier(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "experiment_id": "EXP_2026_V1",
            "protocol_version": "v1.0",
            "case_set_hash": "abc123def456",
            "conditions": ["B1_uploaded_current", "T_full"],
            "replicates": 2,
            "random_seed": 12345,
            "release_gates": {"min_accuracy_delta": 0.15}
        }
        self.gate_result = {
            "release_decision": "PASS_RELEASE",
            "all_gates_passed": True,
            "gate_details": {}
        }
        self.stats = {
            "paired_sample_size": 40,
            "main_comparison": {
                "stats": {
                    "mean_difference": 0.25,
                    "ci_lower": 0.18,
                    "ci_upper": 0.32,
                    "p_value": 0.001,
                    "is_significant": True
                }
            }
        }
        self.adjudication = {"inter_rater_agreement": 0.90, "total_pairs_reviewed": 10}
        self.regression = {"configurations_tested": 4, "total_matrix_runs": 8, "status_distribution": {"complete": 5}}

    def test_01_complete_dossier_validates(self):
        """Pass path: All permanent stamps and traceable claims produce a valid dossier."""
        dossier = generate_evidence_dossier(
            self.manifest, self.gate_result, self.stats,
            self.adjudication, self.regression,
            skill_commit_hash="ecc8c49",
            limitations=["Live web tier not evaluated yet."],
            blocked_rates={"BLOCKED_SOURCE": 0.02},
            failure_rates={"FAIL_PRODUCT": 0.01}
        )
        self.assertEqual(dossier["release_decision"], "PASS_RELEASE")
        self.assertTrue(dossier["all_gates_passed"])
        self.assertEqual(dossier["permanent_stamps"]["skill_commit_hash"], "ecc8c49")
        self.assertEqual(dossier["measured_claims"]["accuracy_delta"], 0.25)
        self.assertTrue(dossier["measured_claims"]["is_statistically_significant"])
        self.assertIn("Live web tier", dossier["disclosed_limitations"][0])
        self.assertEqual(dossier["blocked_rates"]["BLOCKED_SOURCE"], 0.02)

        trace = validate_dossier_claim_traceability(dossier)
        self.assertTrue(trace["is_traceable"])
        self.assertEqual(trace["claim_status"], "VERIFIED_TRACEABLE")

    def test_02_adversarial_missing_traceability_downgrades_claim(self):
        """Adversarial path: Removing raw-run linkage downgrades claim to DOWNGRADED_UNVERIFIABLE."""
        dossier = generate_evidence_dossier(
            self.manifest, self.gate_result, self.stats,
            self.adjudication, self.regression,
            skill_commit_hash="ecc8c49"
        )
        # Tamper: remove raw run availability
        dossier["claim_traceability"]["raw_run_artifacts_available"] = False

        trace = validate_dossier_claim_traceability(dossier)
        self.assertFalse(trace["is_traceable"])
        self.assertEqual(trace["claim_status"], "DOWNGRADED_UNVERIFIABLE")
        self.assertTrue(any("Raw run" in i for i in trace["issues"]))

    def test_03_adversarial_readme_praise_before_gate_clearance(self):
        """Adversarial path: README with improvement claims before gates pass is flagged."""
        failed_gate = {"release_decision": "FAIL_BLOCKED", "all_gates_passed": False}
        dossier = generate_evidence_dossier(
            self.manifest, failed_gate, self.stats,
            self.adjudication, self.regression,
            skill_commit_hash="ecc8c49"
        )
        bad_readme = "# Shopaholic Skill\nThis skill provides proven improvement over baseline approaches."
        res = validate_readme_wording_compliance(bad_readme, dossier)
        self.assertFalse(res["is_compliant"])
        self.assertTrue(any("proven improvement" in i for i in res["issues"]))

        # Good README without claims passes
        good_readme = "# Shopaholic Skill\nExperimental evaluation pending. See evidence dossier for details."
        res2 = validate_readme_wording_compliance(good_readme, dossier)
        self.assertTrue(res2["is_compliant"])

if __name__ == "__main__":
    unittest.main()
