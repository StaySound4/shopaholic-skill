#!/usr/bin/env python3
"""Deterministic automated scorer for objective case assertions.
Evaluates machine-checkable evaluation metrics directly from run artifacts
(run-record.schema.json) and seed case assertions without pre-assigned condition scores.
Evaluates standard errata, certification unmasking, SKU identity, budget constraints,
and sensitivity math.
"""
import re
from typing import Any, Dict, List, Optional

SUPPORTED_ASSERTION_TYPES = {
    "standards_errata",
    "certification_unmasking",
    "sku_identity",
    "budget_constraint",
    "sensitivity_math",
    "round_count_limit"
}

UNMASKING_KEYWORDS = [
    "uncertified",
    "not certified",
    "marketing claim",
    "not in official registry",
    "unverified claim",
    "fake",
    "false claim",
    "not vesa certified",
    "unmasked"
]

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
            "passed": None, # Strictly distinct from True or False
            "failure_reason": f"Unknown or custom assertion type '{atype}' skipped gracefully without failing."
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
        
        # Must explicitly detect unmasking keywords debunking the claim
        has_unmasking_keyword = any(kw in raw_output.lower() for kw in UNMASKING_KEYWORDS)
        
        if must_unmask and not has_unmasking_keyword:
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Failed to unmask uncertified claim '{unmasked_claim}' (merely echoed without debunking keyword)."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    elif atype == "sku_identity":
        expected_model = assertion.get("expected_model", "")
        prohibited_confused_model = assertion.get("prohibited_confused_model", "")
        
        if prohibited_confused_model and prohibited_confused_model.lower() in raw_output.lower():
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Confused SKU/model '{prohibited_confused_model}' in recommendation."
            }
        if expected_model and expected_model.lower() not in raw_output.lower():
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Missing expected target SKU/model '{expected_model}'."
            }
        return {
            "case_id": case_id,
            "run_id": run_id,
            "assertion_type": atype,
            "status": "PASS",
            "passed": True,
            "failure_reason": None
        }

    elif atype == "sensitivity_math":
        expected_flip = assertion.get("expected_flip_weight")
        tolerance = assertion.get("tolerance", 0.05)
        
        # Check sensitivity record in decision record or parsed math in text
        flip_observed = decision_record.get("sensitivity_flip_weight")
        if flip_observed is None:
            # Try parsing from raw output e.g. 'flip point: 0.40' or 'w1 = 0.4'
            m = re.search(r"(?i)flip\s*(?:point|weight)?\s*[:=]\s*([0-9.]+)", raw_output)
            if m:
                try:
                    flip_observed = float(m.group(1))
                except ValueError:
                    flip_observed = None

        if flip_observed is None or (expected_flip is not None and abs(flip_observed - expected_flip) > tolerance):
            return {
                "case_id": case_id,
                "run_id": run_id,
                "assertion_type": atype,
                "status": "FAIL",
                "passed": False,
                "failure_reason": f"Sensitivity flip point calculation mismatch: observed {flip_observed}, expected {expected_flip} (+/- {tolerance})."
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
        "status": "NOT_ADJUDICABLE",
        "passed": None,
        "failure_reason": "Unhandled assertion condition."
    }

def score_run_record(
    run_record: Dict[str, Any],
    assertions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Scores a full run record against a collection of objective assertions."""
    results = [evaluate_single_assertion(a, run_record) for a in assertions]
    total_assertions = len(results)
    passed_assertions = sum(1 for r in results if r["passed"] is True)
    failed_assertions = sum(1 for r in results if r["passed"] is False)
    unadjudicated_assertions = sum(1 for r in results if r["passed"] is None)

    adjudicated_total = passed_assertions + failed_assertions
    accuracy_score = passed_assertions / adjudicated_total if adjudicated_total > 0 else 1.0

    return {
        "run_id": run_record.get("run_id", "UNKNOWN"),
        "total_assertions": total_assertions,
        "passed_count": passed_assertions,
        "failed_count": failed_assertions,
        "unadjudicated_count": unadjudicated_assertions,
        "accuracy_score": accuracy_score,
        "assertion_details": results
    }

if __name__ == "__main__":
    print("Deterministic Automated Scorer ready.")
