#!/usr/bin/env python3
"""Test suite for Ticket 31: Build deterministic automated scorers for objective case assertions.
Tests:
1. Pass: Correct standard citations and unmasking of false marketing assertions pass scoring.
2. Fail: Errata standard citation (IEEE 1788) and budget overruns are penalized.
3. Adversarial: Unknown gold assertion field is not scored as wrong.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deterministic_scorer import (
    evaluate_single_assertion,
    score_run_record
)

class TestTicket31Scorer(unittest.TestCase):
    def test_01_pass_standards_errata_and_unmasking(self):
        """Pass path: Output correctly citing IEEE 1789 and unmasking uncertified HDR1000 passes."""
        run_record = {
            "run_id": "RUN-001",
            "raw_output": "The monitor complies with IEEE 1789 flicker standard. Note: VESA HDR1000 is an uncertified marketing claim not found in official registry.",
            "decision_record": {"selected_candidate_price": 2499.0},
            "round_count": 2
        }
        assertions = [
            {
                "case_id": "CASE-01",
                "assertion_type": "standards_errata",
                "expected_standard": "IEEE 1789",
                "prohibited_errata": "IEEE 1788"
            },
            {
                "case_id": "CASE-01",
                "assertion_type": "certification_unmasking",
                "unmasked_claim": "VESA HDR1000",
                "must_unmask": True
            },
            {
                "case_id": "CASE-01",
                "assertion_type": "budget_constraint",
                "max_budget": 3000.0
            }
        ]
        score = score_run_record(run_record, assertions)
        self.assertEqual(score["passed_count"], 3)
        self.assertEqual(score["failed_count"], 0)
        self.assertEqual(score["accuracy_score"], 1.0)

    def test_02_penalize_obsolete_standards_and_budget_violations(self):
        """Fail path: Output containing prohibited errata or exceeding budget fails."""
        run_record = {
            "run_id": "RUN-002",
            "raw_output": "This display meets the IEEE 1788 low flicker certification.",
            "decision_record": {"selected_candidate_price": 4500.0}
        }
        assertions = [
            {
                "case_id": "CASE-02",
                "assertion_type": "standards_errata",
                "expected_standard": "IEEE 1789",
                "prohibited_errata": "IEEE 1788"
            },
            {
                "case_id": "CASE-02",
                "assertion_type": "budget_constraint",
                "max_budget": 4000.0
            }
        ]
        score = score_run_record(run_record, assertions)
        self.assertEqual(score["passed_count"], 0)
        self.assertEqual(score["failed_count"], 2)
        self.assertEqual(score["accuracy_score"], 0.0)

    def test_03_adversarial_unknown_gold_field_not_scored_wrong(self):
        """Adversarial path: Unknown assertion type must not be falsely penalized."""
        run_record = {"run_id": "RUN-003", "raw_output": "Standard test output."}
        unknown_assertion = {
            "case_id": "CASE-03",
            "assertion_type": "custom_future_metric_xyz",
            "expected_value": 42
        }
        res = evaluate_single_assertion(unknown_assertion, run_record)
        self.assertEqual(res["status"], "NOT_ADJUDICABLE")
        self.assertTrue(res["passed"])

if __name__ == "__main__":
    unittest.main()
