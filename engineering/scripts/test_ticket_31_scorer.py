#!/usr/bin/env python3
"""Test suite for Ticket 31: Build deterministic automated scorers for objective case assertions.
Tests:
1. Pass: Correct standard citations, HDR unmasking with debunking keyword, SKU identity, and sensitivity math pass.
2. Fail: Obsolete standards, echoing claim without unmasking, SKU confusion, and sensitivity math error fail.
3. Adversarial: Unknown gold assertion field yields NOT_ADJUDICABLE and is strictly distinguished from pass/fail.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deterministic_scorer import (
    evaluate_single_assertion,
    score_run_record
)

class TestTicket31Scorer(unittest.TestCase):
    def test_01_pass_all_supported_assertion_types(self):
        """Pass path: Full pass on standards, unmasking, SKU, sensitivity math, and budget."""
        run_record = {
            "run_id": "RUN-001",
            "raw_output": (
                "Recommending Dell U2723QE display. It conforms to IEEE 1789 low-flicker standard. "
                "Warning: VESA HDR1000 is an uncertified marketing claim not in official registry. "
                "Calculated flip point: 0.40."
            ),
            "decision_record": {
                "selected_candidate_price": 2499.0,
                "sensitivity_flip_weight": 0.40
            },
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
                "assertion_type": "sku_identity",
                "expected_model": "Dell U2723QE",
                "prohibited_confused_model": "Dell U2720Q"
            },
            {
                "case_id": "CASE-01",
                "assertion_type": "sensitivity_math",
                "expected_flip_weight": 0.40,
                "tolerance": 0.02
            },
            {
                "case_id": "CASE-01",
                "assertion_type": "budget_constraint",
                "max_budget": 3000.0
            }
        ]
        score = score_run_record(run_record, assertions)
        self.assertEqual(score["passed_count"], 5)
        self.assertEqual(score["failed_count"], 0)
        self.assertEqual(score["unadjudicated_count"], 0)
        self.assertEqual(score["accuracy_score"], 1.0)

    def test_02_penalize_failures_and_false_unmasking(self):
        """Fail path: Merely echoing claim without unmasking, confusing SKU, or wrong math fails."""
        run_record = {
            "run_id": "RUN-002",
            "raw_output": (
                "Recommending Dell U2720Q display. It features incredible VESA HDR1000 high dynamic range. "
                "Conforms to IEEE 1788 standard. Flip point: 0.85."
            ),
            "decision_record": {
                "selected_candidate_price": 4500.0,
                "sensitivity_flip_weight": 0.85
            }
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
                "assertion_type": "certification_unmasking",
                "unmasked_claim": "VESA HDR1000",
                "must_unmask": True
            },
            {
                "case_id": "CASE-02",
                "assertion_type": "sku_identity",
                "expected_model": "Dell U2723QE",
                "prohibited_confused_model": "Dell U2720Q"
            },
            {
                "case_id": "CASE-02",
                "assertion_type": "sensitivity_math",
                "expected_flip_weight": 0.40
            },
            {
                "case_id": "CASE-02",
                "assertion_type": "budget_constraint",
                "max_budget": 4000.0
            }
        ]
        score = score_run_record(run_record, assertions)
        self.assertEqual(score["passed_count"], 0)
        self.assertEqual(score["failed_count"], 5)
        self.assertEqual(score["accuracy_score"], 0.0)

    def test_03_adversarial_not_adjudicable_isolated_from_passing_score(self):
        """Adversarial path: Unknown assertion field is NOT_ADJUDICABLE and does not inflate passed_count."""
        run_record = {"run_id": "RUN-003", "raw_output": "Standard test output."}
        unknown_assertion = {
            "case_id": "CASE-03",
            "assertion_type": "custom_future_metric_xyz",
            "expected_value": 42
        }
        res = evaluate_single_assertion(unknown_assertion, run_record)
        self.assertEqual(res["status"], "NOT_ADJUDICABLE")
        self.assertIsNone(res["passed"])

        score = score_run_record(run_record, [unknown_assertion])
        self.assertEqual(score["unadjudicated_count"], 1)
        self.assertEqual(score["passed_count"], 0)
        self.assertEqual(score["failed_count"], 0)

if __name__ == "__main__":
    unittest.main()
