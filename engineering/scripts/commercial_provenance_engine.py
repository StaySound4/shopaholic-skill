#!/usr/bin/env python3
"""Commercial relationships, sample provenance, and source conflict adjudication engine.
Attaches canonical commercial metadata (brand_owned, seller, affiliate, sponsored,
advertising, loaner, unknown) and sample provenance (self_purchased, manufacturer_supplied, loaner, not_applicable, unknown)
aligned strictly with source-record.schema.json.
Permits sponsored/brand sources to support own declared specs and transparent measurements with caveats,
strictly prevents them from alone establishing comparative superiority, preserves multi-source conflicts,
and prevents affiliate flags from erasing independently reproducible measured facts.
"""
from typing import Any, Dict, List, Optional, Set

CANONICAL_COMMERCIAL_RELATIONSHIPS = {
    "brand_owned",
    "seller",
    "affiliate",
    "sponsored",
    "advertising",
    "loaner",
    "unknown"
}

CANONICAL_SAMPLE_PROVENANCE = {
    "not_applicable",
    "self_purchased",
    "manufacturer_supplied",
    "loaner",
    "unknown"
}

def adjudicate_evidence_with_commercial_context(
    claim_target: str,                   # "own_declared_spec", "comparative_superiority", "comparative_durability", "objective_measurement"
    claimed_value: Any,
    evidence_source: Dict[str, Any],
    corroborating_independent_sources: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Evaluates evidence admissibility and confidence under commercial relationship context."""
    # Read commercial_relationships array or fallback to singular field
    raw_rels = evidence_source.get("commercial_relationships")
    if raw_rels is None and "commercial_relationship" in evidence_source:
        raw_rels = [evidence_source["commercial_relationship"]]
    elif raw_rels is None:
        raw_rels = ["unknown"]

    commercial_rels = set(raw_rels)
    sample_prov = evidence_source.get("sample_provenance", "unknown")
    is_method_transparent = evidence_source.get("is_methodology_transparent", False)
    
    is_sponsored_or_brand = bool(commercial_rels.intersection({"brand_owned", "seller", "sponsored", "advertising", "loaner"}))
    is_affiliate = "affiliate" in commercial_rels
    
    # 1. Comparative superiority / durability claims cannot be established alone by sponsored/brand sources
    if is_sponsored_or_brand and claim_target in ["comparative_superiority", "comparative_durability"]:
        has_independent_corroboration = bool(
            corroborating_independent_sources and any(
                s.get("sample_provenance") == "self_purchased" and not bool(set(s.get("commercial_relationships", ["unknown"])).intersection({"brand_owned", "seller", "sponsored", "advertising"}))
                for s in corroborating_independent_sources
            )
        )
        if not has_independent_corroboration:
            return {
                "claim_target": claim_target,
                "admissible": False,
                "confidence": "U",
                "status": "rejected_unsubstantiated_commercial_claim",
                "bias_disclosure": f"Sponsored/brand source ({list(commercial_rels)}) cannot alone establish comparative superiority/durability without independent corroboration.",
                "value_adopted": None
            }

    # 2. Check for multi-source conflicts
    if corroborating_independent_sources:
        independent_measurements = [s.get("measured_value") for s in corroborating_independent_sources if s.get("measured_value") is not None]
        if independent_measurements and claimed_value not in independent_measurements:
            return {
                "claim_target": claim_target,
                "admissible": True,
                "confidence": "B",
                "status": "conflict_disputed",
                "bias_disclosure": f"Multi-source conflict: Commercial claim '{claimed_value}' contradicts independent retail sample measurement '{independent_measurements[0]}'.",
                "value_adopted": independent_measurements[0]  # Prioritize independent measurement
            }

    # 3. Guard against erasing independently reproducible measured facts solely due to affiliate flag
    if (is_affiliate or is_sponsored_or_brand) and is_method_transparent:
        return {
            "claim_target": claim_target,
            "admissible": True,
            "confidence": "A" if is_method_transparent else "B",
            "status": "verified_with_commercial_caveat",
            "bias_disclosure": f"Source has commercial tags ({list(commercial_rels)}), but methodology is transparent and test data is reproducible.",
            "value_adopted": claimed_value
        }

    # 4. Standard own declared spec from brand
    if is_sponsored_or_brand and claim_target in ["own_declared_spec", "objective_measurement"]:
        return {
            "claim_target": claim_target,
            "admissible": True,
            "confidence": "B",
            "status": "accepted_as_manufacturer_spec",
            "bias_disclosure": f"Official declared specification from manufacturer ({list(commercial_rels)}); accepted with manufacturer caveat.",
            "value_adopted": claimed_value
        }

    # 5. Default independent source
    return {
        "claim_target": claim_target,
        "admissible": True,
        "confidence": "S" if sample_prov == "self_purchased" else "A",
        "status": "verified_independent",
        "bias_disclosure": "Independent source without commercial sponsorship.",
        "value_adopted": claimed_value
    }

if __name__ == "__main__":
    print("Commercial Provenance Engine Module ready.")
