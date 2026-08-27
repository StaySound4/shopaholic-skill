#!/usr/bin/env python3
"""Explicit degraded modes and tool/source unavailability engine.
Defines explicit degraded states ('partial', 'blocked', 'source_unavailable') when
essential web search tools, APIs, or regulatory databases are inaccessible.
Strictly prohibits silent fallback to ungrounded memory hallucinations and enforces
confidence degradation (B/U) when secondary fallbacks are used.
"""
from typing import Any, Dict, List, Optional, Set

VALID_DECISION_STATUSES = {"complete", "partial", "source_unavailable", "blocked"}
VALID_EVAL_STATUSES = {"SUCCESS", "PARTIAL_EVIDENCE", "BLOCKED_SOURCE"}

def handle_source_tool_unavailability(
    required_source_id: str,
    is_source_accessible: bool,
    fallback_sources: Optional[List[Dict[str, Any]]] = None,
    is_safety_critical: bool = False
) -> Dict[str, Any]:
    """Handles source availability check and determines degraded mode."""
    if is_source_accessible:
        return {
            "decision_status": "complete",
            "eval_status": "SUCCESS",
            "evidence_grade": "S",
            "blocked_source": None,
            "is_degraded": False,
            "notes": f"Authoritative source {required_source_id} successfully verified."
        }

    # Source is inaccessible
    if not fallback_sources:
        # Complete block -> No evidence available
        return {
            "decision_status": "blocked" if is_safety_critical else "source_unavailable",
            "eval_status": "BLOCKED_SOURCE",
            "evidence_grade": "U",
            "blocked_source": required_source_id,
            "is_degraded": True,
            "retry_eligible": True,
            "notes": f"Mandatory source '{required_source_id}' is inaccessible. Memory hallucination prohibited."
        }

    # Secondary fallback sources available -> Degrade confidence
    best_fallback = fallback_sources[0]
    fallback_role = best_fallback.get("source_role", "unknown")
    
    # Blogs / consumer reviews can NEVER retain S or A grade for regulatory claims
    degraded_grade = "B" if fallback_role == "independent_measurement" else "U"
    
    return {
        "decision_status": "partial",
        "eval_status": "PARTIAL_EVIDENCE",
        "evidence_grade": degraded_grade,
        "blocked_source": required_source_id,
        "fallback_adopted": best_fallback.get("source_id", "unnamed_fallback"),
        "is_degraded": True,
        "retry_eligible": True,
        "notes": f"Authoritative source '{required_source_id}' unavailable; degraded to fallback with grade '{degraded_grade}'."
    }

def validate_degraded_grade_safety(
    claim_type: str,
    original_source_role: str,
    actual_source_role: str,
    assigned_grade: str
) -> bool:
    """Guards against blogs replacing regulators while retaining S grades."""
    if original_source_role in ["regulatory", "voluntary_certification"]:
        if actual_source_role not in ["regulatory", "voluntary_certification"] and assigned_grade in ["S", "A"]:
            # Illegal grade elevation on degraded fallback
            return False
    return True

if __name__ == "__main__":
    print("Degraded Mode Engine Module ready.")
