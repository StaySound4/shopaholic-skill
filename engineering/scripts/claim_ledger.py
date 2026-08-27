#!/usr/bin/env python3
"""Claim and evidence ledger with explicit unknown, disputed, and CMD discrepancy states.
Manages decision-critical claims with precise scoping, contradicting evidence preservation,
and structured Claim-Metric Discrepancy (CMD) pairing.
"""
import argparse, json, sys, uuid
from pathlib import Path

def create_claim_record(
    claim_id: str | None,
    claim: str,
    claim_type: str,
    impact: str,
    entity_id: str,
    region_sku: str | None = None,
    revision: str | None = None,
    batch: str | None = None,
    supporting_sources: list[str] | None = None,
    contradicting_sources: list[str] | None = None,
    claimed_value: str | None = None,
    claimed_source_ref: str | None = None,
    measured_value: str | None = None,
    measured_source_ref: str | None = None,
    deviation_type: str | None = None,
    severity: str | None = None,
    source_role_appropriate: bool | None = None,
    freshness_state: str = "current",
    decision_effect: str = "none",
    notes: str | None = None
) -> dict:
    """Constructs and evaluates a structured claim record."""
    cid = claim_id or f"CLM-{uuid.uuid4().hex[:8]}"
    sup = supporting_sources or []
    contra = contradicting_sources or []
    
    # Adjudicate status and evidence_grade
    discrepancy = None
    if claimed_value is not None or measured_value is not None:
        discrepancy = {
            "claimed_value": claimed_value or "unspecified",
            "claimed_source_ref": claimed_source_ref,
            "measured_value": measured_value or "unmeasured",
            "measured_source_ref": measured_source_ref,
            "deviation_type": deviation_type or "other",
            "severity": severity or "minor"
        }
        
    if contra and sup:
        status = "disputed"
        evidence_grade = "B"
    elif contra and not sup:
        status = "disputed"
        evidence_grade = "B"
    elif sup:
        status = "verified"
        evidence_grade = "S" if source_role_appropriate else "A"
    else:
        status = "unverified"
        evidence_grade = "U"
        
    record = {
        "claim_id": cid,
        "claim": claim,
        "claim_type": claim_type,
        "impact": impact,
        "scope": {
            "entity_id": entity_id,
            "region_sku": region_sku,
            "revision": revision,
            "batch": batch
        },
        "status": status,
        "evidence_grade": evidence_grade,
        "supporting_sources": sup,
        "contradicting_sources": contra,
        "source_role_appropriate": source_role_appropriate,
        "freshness_state": freshness_state,
        "decision_effect": decision_effect,
        "discrepancy": discrepancy,
        "notes": notes
    }
    
    return record

def validate_claim_ledger_entry(record: dict) -> list[str]:
    """Validates a claim record against required invariants."""
    errors = []
    required = ["claim_id", "claim", "claim_type", "impact", "status", "evidence_grade", "scope"]
    for req in required:
        if req not in record or record[req] is None:
            errors.append(f"Missing required property: {req}")
            
    if "scope" in record:
        if not isinstance(record["scope"], dict) or "entity_id" not in record["scope"]:
            errors.append("Scope must be an object containing 'entity_id'")
            
    status = record.get("status")
    if status not in ["verified", "disputed", "unverified"]:
        errors.append(f"Invalid status '{status}'")
        
    grade = record.get("evidence_grade")
    if grade not in ["S", "A", "B", "U"]:
        errors.append(f"Invalid evidence_grade '{grade}'")
        
    # Invariant: If there are contradicting sources and no resolution, status cannot be verified
    if record.get("contradicting_sources") and status == "verified":
        errors.append("Contradicting sources exist but claim is marked verified without resolution")
        
    # Invariant: If no supporting sources exist, status must be unverified or disputed
    if not record.get("supporting_sources") and status == "verified":
        errors.append("No supporting sources provided but claim is marked verified")
        
    return errors

if __name__ == "__main__":
    print("Claim Ledger Module ready.")
