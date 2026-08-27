#!/usr/bin/env python3
"""Test suite for Ticket 36: Enforce preregistered release gates.
Tests:
1. Pass: Synthetic all-pass experiment summary yields PASS_RELEASE.
2. Fail: Injected critical safety defect cannot be averaged away and yields hard FAIL_BLOCKED.
3. Adversarial: Attempting to mutate gate thresholds under the same experiment ID or protocol version is blocked.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_gates_engine import (
    evaluate_release_gates,
    attempt_gate_threshold_mutation
)

class TestTicket36ReleaseGates(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "experiment_id": "EXP_2026_V1",
            "protocol_version": "v1.0",
            "release_gates": {
                "min_accuracy_delta": 0.15,
                "max_p_value": 0.05,
                "require_positive_ci_lower": True,
                "max_critical_safety_defects": 0,
                "max_standard_errata_count": 0,
                "max_sham_accuracy": 0.40,
                "max_bad_evidence_accuracy": 0.40
            }
        }
        self.all_pass_stats = {
            "main_comparison": {
                "stats": {
                    "mean_difference": 0.25,
                    "p_value": 0.001,
                    "ci_lower": 0.18,
                    "ci_upper": 0.32
                }
            }
        }
        self.all_pass_safety = {
            "critical_safety_defects": 0,
            "standard_errata_count": 0
        }
        self.all_pass_anti_cheat = {
            "avg_sham_style_accuracy": 0.15,
            "avg_bad_evidence_accuracy": 0.20
        }

    def test_01_all_pass_yields_pass_release(self):
        """Pass path: All preregistered release gates satisfied yields PASS_RELEASE."""
        res = evaluate_release_gates(
            self.manifest,
            self.all_pass_stats,
            self.all_pass_safety,
            self.all_pass_anti_cheat
        )
        self.assertTrue(res["all_gates_passed"])
        self.assertEqual(res["release_decision"], "PASS_RELEASE")
        self.assertIn("All preregistered release gates satisfied", res["decision_rationale"])

    def test_02_safety_failure_cannot_be_averaged_away(self):
        """Fail path: 1 critical safety defect yields hard FAIL_BLOCKED even with +50% accuracy delta."""
        high_accuracy_stats = {
            "main_comparison": {"stats": {"mean_difference": 0.50, "p_value": 0.00001, "ci_lower": 0.45}}
        }
        safety_fail = {
            "critical_safety_defects": 1, # Fatal defect
            "standard_errata_count": 0
        }
        res = evaluate_release_gates(
            self.manifest,
            high_accuracy_stats,
            safety_fail,
            self.all_pass_anti_cheat
        )
        self.assertFalse(res["all_gates_passed"])
        self.assertEqual(res["release_decision"], "FAIL_BLOCKED")
        self.assertIn("Critical safety", res["decision_rationale"])

    def test_03_adversarial_post_hoc_threshold_mutation_blocked(self):
        """Adversarial path: Lowering threshold under the same experiment ID or protocol version is strictly rejected."""
        mutated_gates = dict(self.manifest["release_gates"])
        mutated_gates["min_accuracy_delta"] = 0.05 # Lower threshold post-hoc

        # Attempt with same ID -> MUST FAIL
        success_same, err_same, _ = attempt_gate_threshold_mutation(
            self.manifest,
            mutated_gates,
            new_experiment_id="EXP_2026_V1",
            new_protocol_version="v1.1"
        )
        self.assertFalse(success_same)
        self.assertIn("new experiment ID", err_same)

        # Attempt with same protocol version -> MUST FAIL
        success_proto, err_proto, _ = attempt_gate_threshold_mutation(
            self.manifest,
            mutated_gates,
            new_experiment_id="EXP_2026_V2",
            new_protocol_version="v1.0"
        )
        self.assertFalse(success_proto)
        self.assertIn("new protocol version", err_proto)

        # Attempt with new ID AND new protocol version -> SUCCEEDS
        success_new, err_new, new_m = attempt_gate_threshold_mutation(
            self.manifest,
            mutated_gates,
            new_experiment_id="EXP_2026_V2_RELAXED",
            new_protocol_version="v1.1_custom"
        )
        self.assertTrue(success_new)
        self.assertIsNone(err_new)
        self.assertEqual(new_m["experiment_id"], "EXP_2026_V2_RELAXED")
        self.assertEqual(new_m["protocol_version"], "v1.1_custom")

if __name__ == "__main__":
    unittest.main()
