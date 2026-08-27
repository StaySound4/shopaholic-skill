#!/usr/bin/env python3
"""Evidence role router and suitability engine.
Replaces universal L1-L4 hierarchy with claim-specific evidence routing:
evaluates whether a source role is appropriate to prove a specific claim type.
"""
import argparse, json, sys
from pathlib import Path

# Mapping of what claim types each source role is appropriate to prove
APPROPRIATE_ROLE_MAPPINGS = {
    "price_and_availability": ["market_price"],
    "declared_dimension_interface": ["official_primary", "regulatory"],
    "legal_market_entry": ["regulatory"],
    "safety_certification": ["regulatory", "voluntary_certification"],
    "voluntary_technical_tier": ["voluntary_certification"],
    "measured_performance": ["independent_measurement"],
    "component_sourcing_teardown": ["teardown_forensic", "independent_measurement"],
    "field_failure_rate_recall": ["field_repair", "regulatory"],
    "corporate_ownership_provenance": ["corporate_registry", "regulatory"],
    "comparative_superiority": ["independent_measurement"],
    "long_term_durability": ["field_repair", "independent_measurement"]
}

def is_source_role_appropriate(source_role: str, claim_type: str) -> bool:
    """Evaluates whether the given source_role is epistemically appropriate to support the claim_type."""
    allowed_roles = APPROPRIATE_ROLE_MAPPINGS.get(claim_type, [])
    return source_role in allowed_roles

def evaluate_evidence_packet_for_claim(claim_type: str, sources: list[dict]) -> dict:
    """Evaluates a collection of sources for a specific claim.
    Returns appropriateness, count breakdown, and whether the claim can be verified.
    """
    total_sources = len(sources)
    if total_sources == 0:
        return {
            "claim_type": claim_type,
            "appropriate_source_count": 0,
            "total_source_count": 0,
            "overall_appropriate": False,
            "can_verify": False,
            "reasons": ["No sources provided"]
        }
        
    appropriate_sources = []
    inappropriate_sources = []
    
    for s in sources:
        role = s.get("source_role", "unknown")
        if is_source_role_appropriate(role, claim_type):
            appropriate_sources.append(s)
        else:
            inappropriate_sources.append(s)
            
    app_count = len(appropriate_sources)
    reasons = []
    
    # Check if we have at least one appropriate source
    if app_count == 0:
        reasons.append(
            f"No source has an appropriate role for '{claim_type}'. Received roles: {[s.get('source_role') for s in sources]}"
        )
        can_verify = False
    else:
        can_verify = True
        
    return {
        "claim_type": claim_type,
        "appropriate_source_count": app_count,
        "total_source_count": total_sources,
        "overall_appropriate": app_count > 0,
        "can_verify": can_verify,
        "reasons": reasons,
        "appropriate_sources": appropriate_sources,
        "inappropriate_sources": inappropriate_sources
    }

if __name__ == "__main__":
    print("Evidence Role Router ready.")
