#!/usr/bin/env python3
"""Scoped safety-signal adjudication engine.
Implements a 7-stage risk adjudication state machine, eliminates mechanical
incident-count vetoes, enforces exposure denominator awareness, and reserves
hard exclusions strictly for verified, scoped safety/recall evidence.
"""
from typing import Any, Dict, List, Optional

# Decision impact categories
DECISION_IMPACTS = {
    "hard_exclude",            # Mandatory product exclusion due to active recall or confirmed hazard
    "scoped_exclude_batch",    # Exclude only the affected batch/revision, allow clean revisions
    "risk_signal_disclosure",  # Disclose unverified/isolated risk in decision record without veto
    "watch_point",             # Low statistical significance relative to exposure volume
    "dismissed_user_misuse"    # Attributed to non-OEM accessory or gross misuse
}

def adjudicate_safety_signal(
    signal_id: str,
    product_entity: Dict[str, Any],
    source_type: str,            # "official_recall", "lab_test", "court_case", "user_forum", "social_media"
    incident_description: str,
    reported_incidents: List[Dict[str, Any]],
    exposure_volume: Optional[int] = None,     # Total sales / installed units denominator
    affected_revisions: Optional[List[str]] = None,
    affected_batches: Optional[List[str]] = None,
    has_official_regulatory_action: bool = False,
    is_plausible_user_misuse_or_non_oem: bool = False
) -> Dict[str, Any]:
    """Runs a signal through the 7-stage risk adjudication state machine."""
    current_revision = product_entity.get("revision", "Rev A")
    current_batch = product_entity.get("batch_window")
    
    # Stage 1: Discovered
    stage_1 = {"stage": "1_discovered", "signal_id": signal_id, "desc": incident_description}
    
    # Stage 2: Authenticity
    is_authoritative = source_type in ["official_recall", "lab_test", "court_case"]
    stage_2 = {
        "stage": "2_authenticity",
        "source_type": source_type,
        "is_authoritative": is_authoritative,
        "is_anecdotal": source_type in ["user_forum", "social_media"]
    }
    
    # Stage 3: Deduplication
    unique_users = set()
    deduped_incidents = []
    for inc in reported_incidents:
        user = inc.get("user_id") or inc.get("source_post_url")
        if user not in unique_users:
            unique_users.add(user)
            deduped_incidents.append(inc)
    dedup_count = len(deduped_incidents)
    stage_3 = {
        "stage": "3_deduplication",
        "raw_count": len(reported_incidents),
        "deduped_count": dedup_count
    }
    
    # Stage 4: Scope / Batch isolation
    is_scoped_to_specific_revision = bool(affected_revisions and current_revision not in affected_revisions)
    is_scoped_to_specific_batch = bool(affected_batches and current_batch and current_batch not in affected_batches)
    affects_current_product = not (is_scoped_to_specific_revision or is_scoped_to_specific_batch)
    stage_4 = {
        "stage": "4_scope_batch",
        "current_revision": current_revision,
        "affected_revisions": affected_revisions,
        "affects_current_product": affects_current_product
    }
    
    # Stage 5: Causal & Misuse Check
    stage_5 = {
        "stage": "5_causal_misuse_check",
        "is_plausible_user_misuse": is_plausible_user_misuse_or_non_oem
    }
    
    # Stage 6: Regulatory Action
    stage_6 = {
        "stage": "6_regulatory_action",
        "has_official_recall": has_official_regulatory_action
    }
    
    # Stage 7: Decision Impact
    if has_official_regulatory_action and affects_current_product:
        decision_impact = "hard_exclude"
        rationale = "Official regulatory recall in effect for current product revision/batch."
    elif has_official_regulatory_action and not affects_current_product:
        decision_impact = "scoped_exclude_batch"
        rationale = f"Official recall isolated to earlier revisions/batches ({affected_revisions}); current {current_revision} is cleared."
    elif is_plausible_user_misuse_or_non_oem:
        decision_impact = "dismissed_user_misuse"
        rationale = "Incident causally attributed to non-OEM accessory usage or external misuse."
    elif not is_authoritative:
        # Anecdotal report
        decision_impact = "risk_signal_disclosure"
        rationale = "Unverified anecdotal report: recorded as transparent risk signal and trigger for further scrutiny without instant veto."
    else:
        # Verified defect without recall - evaluate exposure denominator
        if exposure_volume and exposure_volume > 100000 and dedup_count <= 5:
            decision_impact = "watch_point"
            rationale = f"Low statistical rate ({dedup_count} incidents in ~{exposure_volume} units); maintained as watch point."
        else:
            decision_impact = "hard_exclude" if affects_current_product else "scoped_exclude_batch"
            rationale = f"Verified defect impacting {current_revision}."

    stage_7 = {
        "stage": "7_decision_impact",
        "impact": decision_impact,
        "rationale": rationale,
        "hard_exclude": decision_impact == "hard_exclude"
    }

    return {
        "signal_id": signal_id,
        "decision_impact": decision_impact,
        "hard_exclude": decision_impact == "hard_exclude",
        "rationale": rationale,
        "stages": [stage_1, stage_2, stage_3, stage_4, stage_5, stage_6, stage_7]
    }

if __name__ == "__main__":
    print("Safety Adjudication Engine Module ready.")
