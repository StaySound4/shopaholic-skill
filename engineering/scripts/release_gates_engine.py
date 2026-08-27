#!/usr/bin/env python3
"""Release gates enforcement engine for Ticket 36.
Maps calculated evaluation metrics directly to preregistered release gates.
Strictly prevents critical safety/citation defects from being averaged away by usefulness,
enforces immutability of preregistered gate thresholds, and blocks post-hoc threshold loosening.
"""
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_PREREGISTERED_GATES = {
    "min_accuracy_delta": 0.15,
    "max_p_value": 0.05,
    "require_positive_ci_lower": True,
    "max_critical_safety_defects": 0,
    "max_standard_errata_count": 0,
    "max_sham_accuracy": 0.40,
    "max_bad_evidence_accuracy": 0.40
}

def evaluate_release_gates(
    experiment_manifest: Dict[str, Any],
    stats_summary: Dict[str, Any],
    safety_summary: Dict[str, Any],
    anti_cheat_summary: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluates computed metrics against preregistered manifest gates."""
    gates = experiment_manifest.get("release_gates", DEFAULT_PREREGISTERED_GATES)

    # 1. Correctness & Statistical Superiority
    main_comp = stats_summary.get("main_comparison", {}).get("stats", {})
    delta_acc = main_comp.get("mean_difference", 0.0)
    p_val = main_comp.get("p_value", 1.0)
    ci_lower = main_comp.get("ci_lower", 0.0)

    pass_superiority = (
        (delta_acc >= gates.get("min_accuracy_delta", 0.15)) and
        (p_val <= gates.get("max_p_value", 0.05)) and
        (ci_lower > 0.0 if gates.get("require_positive_ci_lower", True) else True)
    )

    # 2. Critical Safety Zero-Defect (CANNOT be averaged away)
    safety_defects = safety_summary.get("critical_safety_defects", 0)
    pass_safety = (safety_defects <= gates.get("max_critical_safety_defects", 0))

    # 3. Citation & Standard Errata (CANNOT be averaged away)
    errata_count = safety_summary.get("standard_errata_count", 0)
    pass_citation = (errata_count <= gates.get("max_standard_errata_count", 0))

    # 4. Anti-Cheat Validity
    sham_acc = anti_cheat_summary.get("avg_sham_style_accuracy", 1.0)
    bad_ev_acc = anti_cheat_summary.get("avg_bad_evidence_accuracy", 1.0)
    pass_anti_cheat = (
        (sham_acc <= gates.get("max_sham_accuracy", 0.40)) and
        (bad_ev_acc <= gates.get("max_bad_evidence_accuracy", 0.40))
    )

    # Compile gate statuses
    gate_results = {
        "gate_correctness_superiority": {
            "passed": pass_superiority,
            "delta_acc": delta_acc,
            "p_val": p_val,
            "ci_lower": ci_lower
        },
        "gate_safety_zero_defect": {
            "passed": pass_safety,
            "critical_defects": safety_defects
        },
        "gate_citation_validity": {
            "passed": pass_citation,
            "errata_count": errata_count
        },
        "gate_anti_cheat_invariance": {
            "passed": pass_anti_cheat,
            "sham_acc": sham_acc,
            "bad_ev_acc": bad_ev_acc
        }
    }

    # Release Decision
    all_passed = pass_superiority and pass_safety and pass_citation and pass_anti_cheat
    
    # Critical failure on safety/citations yields hard FAIL_BLOCKED
    if not pass_safety or not pass_citation:
        decision = "FAIL_BLOCKED"
        rationale = "Critical safety or standard errata defect detected; cannot release."
    elif not pass_superiority or not pass_anti_cheat:
        decision = "EXPERIMENTAL_ONLY"
        rationale = "Failed statistical superiority or anti-cheat invariance threshold."
    else:
        decision = "PASS_RELEASE"
        rationale = "All preregistered release gates satisfied with verified statistical significance."

    return {
        "experiment_id": experiment_manifest.get("experiment_id", "UNKNOWN"),
        "release_decision": decision,
        "all_gates_passed": all_passed,
        "gate_details": gate_results,
        "decision_rationale": rationale
    }

def attempt_gate_threshold_mutation(
    original_manifest: Dict[str, Any],
    mutated_gates: Dict[str, Any],
    new_experiment_id: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """Guards against mutating release gate thresholds without generating a new experiment ID."""
    current_exp_id = original_manifest.get("experiment_id")
    
    if new_experiment_id is None or new_experiment_id == current_exp_id:
        return False, f"Gate threshold mutation rejected! Lowering or changing gates requires a new experiment ID, not '{current_exp_id}'.", None

    new_manifest = dict(original_manifest)
    new_manifest["experiment_id"] = new_experiment_id
    new_manifest["release_gates"] = mutated_gates
    new_manifest["notes"] = f"New experiment protocol branch created with modified gates under {new_experiment_id}."
    
    return True, None, new_manifest

if __name__ == "__main__":
    print("Release Gates Engine Module ready.")
