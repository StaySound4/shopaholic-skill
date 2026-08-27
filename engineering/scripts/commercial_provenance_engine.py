#!/usr/bin/env python3
"""Commercial relationships, sample provenance, and source conflict adjudication engine.
Attaches commercial metadata (brand, affiliate, sponsored, loaner, self-purchased retail)
and sample provenance to evidence packets. Permits sponsored sources to support own
declared specs/transparent measurements with disclosed caveat, strictly prevents them
from alone establishing comparative superiority, preserves multi-source conflicts,
and prevents affiliate flags from erasing independently reproducible measured facts.
"""
from typing import Any, Dict, List, Optional

COMMERCIAL_RELATIONSHIPS = {
    "brand_official",
    "seller_promotional",
    "affiliate_commission",
    "sponsored_paid",
    "brand_loaner_unit",
    "self_purchased_retail",
    "independent_nonprofit",
    "unknown"
}

SAMPLE_PROVENANCES = {
    "retail_store_anonymously_bought",
    "manufacturer_cherry_picked_loaner",
    "pr_review_unit",
    "unknown"
}

def adjudicate_evidence_with_commercial_context(
    claim_target: str,                   # "own_declared_spec", "comparative_superiority", "comparative_durability", "objective_measurement"
    claimed_value: Any,
    evidence_source: Dict[str, Any],
    corroborating_independent_sources: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Evaluates evidence admissibility and confidence under commercial relationship context."""
    commercial_rel = evidence_source.get("commercial_relationship", "unknown")
    sample_prov = evidence_source.get("sample_provenance", "unknown")
    is_method_transparent = evidence_source.get("is_methodology_transparent", False)
    
    is_sponsored_or_brand = commercial_rel in ["brand_official", "seller_promotional", "sponsored_paid", "brand_loaner_unit"]
    is_affiliate = commercial_rel == "affiliate_commission"
    
    # 1. Comparative superiority / durability claims cannot be established alone by sponsored/brand sources
    if is_sponsored_or_brand and claim_target in ["comparative_superiority", "comparative_durability"]:
        has_independent_corroboration = bool(
            corroborating_independent_sources and any(
                s.get("commercial_relationship") in ["self_purchased_retail", "independent_nonprofit"] for s in corroborating_independent_sources
            )
        )
        if not has_independent_corroboration:
            return {
                "claim_target": claim_target,
                "admissible": False,
                "confidence": "U",
                "status": "rejected_unsubstantiated_commercial_claim",
                "bias_disclosure": f"Sponsored/brand source ({commercial_rel}) cannot alone establish comparative superiority/durability without independent lab corroboration.",
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
                "value_adopted": independent_measurements[0]  # Prioritize independent retail measurement
            }

    # 3. Guard against erasing independently reproducible measured facts solely due to affiliate flag
    if (is_affiliate or is_sponsored_or_brand) and is_method_transparent:
        return {
            "claim_target": claim_target,
            "admissible": True,
            "confidence": "A" if is_method_transparent else "B",
            "status": "verified_with_commercial_caveat",
            "bias_disclosure": f"Source has commercial tag ({commercial_rel}), but methodology is transparent and test data is reproducible.",
            "value_adopted": claimed_value
        }

    # 4. Standard own declared spec from brand
    if is_sponsored_or_brand and claim_target in ["own_declared_spec", "objective_measurement"]:
        return {
            "claim_target": claim_target,
            "admissible": True,
            "confidence": "B",
            "status": "accepted_as_manufacturer_spec",
            "bias_disclosure": f"Official declared specification from manufacturer ({commercial_rel}); accepted with manufacturer caveat.",
            "value_adopted": claimed_value
        }

    # 5. Default independent source
    return {
        "claim_target": claim_target,
        "admissible": True,
        "confidence": "S" if sample_prov == "retail_store_anonymously_bought" else "A",
        "status": "verified_independent",
        "bias_disclosure": "Independent source without commercial sponsorship.",
        "value_adopted": claimed_value
    }

if __name__ == "__main__":
    print("Commercial Provenance Engine Module ready.")
