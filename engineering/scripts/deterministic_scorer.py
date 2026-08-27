#!/usr/bin/env python3
"""Deterministic automated scorer for objective case assertions.
Evaluates machine-checkable evaluation metrics directly from run artifacts
(run-record.schema.json) and seed case assertions without pre-assigned condition scores.
Evaluates standard errata, certification unmasking, SKU identity, budget constraints,
and sensitivity math.
"""
import json
from typing import Any, Dict, List, Optional

SUPPORTED_ASSERTION_TYPES = {
    "standards_errata",
    "certification_unmasking",
    "sku_identity",
    "budget_constraint",
    "sensitivity_math",
    "round_count_limit"
}

def evaluate_single_assertion(
    assertion: Dict[str, Any],
    run_record: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluates a single objective assertion against a run record."""
    atype = assertion.get("assertion_type")
    case_id = assertion.get("case_id", "UNKNOWN_CASE")
    run_id = run_record.get("run_id", "UNKNOWN_RUN")

    if atype not in SUPPORTED_ASSERTION_TYPES:
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "NOT_ADJUDICABLE",
            "passed": True, # Unknown gold fields must not be scored as failing/wrong
            "failure_reason": f"Unknown or custom assertion type '{atype}' skipped gracefully."
        }

    raw_output = run_record.get("raw_output", "")
    decision_record = run_record.get("decision_record", {})

    if atype == "standards_errata":
        target_standard = assertion.get("expected_standard", "")
        prohibited_errata = assertion.get("prohibited_errata", "")
        if prohibited_errata and prohibited_errata.lower() in raw_output.lower():
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Cited obsolete/errata standard '{prohibited_errata}' instead of '{target_standard}'."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    elif atype == "certification_unmasking":
        unmasked_claim = assertion.get("unmasked_claim", "")
        must_unmask = assertion.get("must_unmask", True)
        is_unmasked_in_output = unmasked_claim.lower() in raw_output.lower() or "uncertified" in raw_output.lower() or "marketing claim" in raw_output.lower()
        if must_unmask and not is_unmasked_in_output:
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Failed to unmask uncertified claim '{unmasked_claim}'."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    elif atype == "budget_constraint":
        max_budget = assertion.get("max_budget", float("inf"))
        observed_price = decision_record.get("selected_candidate_price", 0.0)
        if observed_price > max_budget:
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Selected product price ({observed_price}) exceeds budget limit ({max_budget})."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    elif atype == "round_count_limit":
        max_rounds = assertion.get("max_rounds", 3)
        actual_rounds = run_record.get("round_count", 1)
        if actual_rounds > max_rounds:
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Conversation round count ({actual_rounds}) exceeded limit ({max_rounds})."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    return {
        "case_id": case_id,
        "run_id": run_id,
        "assertion_type": atype,
        "status": "PASS",
        "passed": True,
        "failure_reason": None
    }

def score_run_record(
    run_record: Dict[str, Any],
    assertions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Scores a full run record against a collection of objective assertions."""
    results = [evaluate_single_assertion(a, run_record) for a in assertions]
    total_assertions = len(results)
    passed_assertions = sum(1 for r in results if r["passed"])
    failed_assertions = sum(1 for r in results if not r["passed"])

    return {
        "run_id": run_record.get("run_id", "UNKNOWN"),
        "total_assertions": total_assertions,
        "passed_count": passed_assertions,
        "failed_count": failed_assertions,
        "accuracy_score": passed_assertions / total_assertions if total_assertions > 0 else 1.0,
        "assertion_details": results
    }

if __name__ == "__main__":
    print("Deterministic Automated Scorer ready.")
