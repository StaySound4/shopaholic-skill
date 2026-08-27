#!/usr/bin/env python3
"""Evidence confidence semantics (S/A/B/U) and maturity pool separation engine.
Evaluates evidence coverage independently from market maturity, ensuring:
1. S/A/B/U grades reflect decision-critical claim verification.
2. Maturity pools (mature, conditional, watch, exclude) reflect operational adoption states.
3. Market age/popularity never artificially elevates an evidence grade with disputed claims.
"""
import argparse, json, sys
from pathlib import Path

def calculate_evidence_grade(claims: list[dict]) -> dict:
    """Computes aggregate S/A/B/U evidence confidence grade from a collection of claim records.
    - S (Authoritative): All critical/high claims verified by appropriate authoritative/lab sources without conflicts.
    - A (Substantial): Critical claims verified with appropriate sources; minor claims have no critical disputes.
    - B (Bounded/Disputed): Unresolved conflicts (disputed) exist, or critical claims rely on single weak sources.
    - U (Unverified): Critical claims lack appropriate evidence or are unverified.
    """
    if not claims:
        return {
            "grade": "U",
            "reason": "Zero claims provided; ungrounded recommendation.",
            "verified_count": 0,
            "disputed_count": 0,
            "unverified_count": 0
        }
        
    critical_claims = [c for c in claims if c.get("impact") in ["critical", "high"]]
    if not critical_claims:
        critical_claims = claims  # Fallback to all claims if none marked critical/high
        
    disputed = [c for c in critical_claims if c.get("status") == "disputed"]
    unverified = [c for c in critical_claims if c.get("status") == "unverified"]
    verified = [c for c in critical_claims if c.get("status") == "verified"]
    
    # Check if any critical claim is unverified
    if unverified:
        return {
            "grade": "U",
            "reason": f"{len(unverified)} critical/high-impact claim(s) are unverified.",
            "verified_count": len(verified),
            "disputed_count": len(disputed),
            "unverified_count": len(unverified)
        }
        
    # Check if any critical claim is disputed
    if disputed:
        return {
            "grade": "B",
            "reason": f"{len(disputed)} critical/high-impact claim(s) have unresolved conflicts/discrepancies.",
            "verified_count": len(verified),
            "disputed_count": len(disputed),
            "unverified_count": len(unverified)
        }
        
    # Check if all verified claims have appropriate source roles
    inappropriate_verified = [c for c in verified if c.get("source_role_appropriate") is False]
    if inappropriate_verified:
        return {
            "grade": "B",
            "reason": f"{len(inappropriate_verified)} verified claim(s) rely on epistemically inappropriate source roles.",
            "verified_count": len(verified),
            "disputed_count": len(disputed),
            "unverified_count": len(unverified)
        }
        
    # S vs A distinction: S requires all critical claims to have grade S sources (authoritative lab/registry)
    all_s_grade = all(c.get("evidence_grade") == "S" for c in verified)
    if all_s_grade and len(verified) >= 1:
        return {
            "grade": "S",
            "reason": "All critical claims independently verified by authoritative/lab registries with zero conflicts.",
            "verified_count": len(verified),
            "disputed_count": len(disputed),
            "unverified_count": len(unverified)
        }
    else:
        return {
            "grade": "A",
            "reason": "Critical claims verified with substantial primary and measurement evidence.",
            "verified_count": len(verified),
            "disputed_count": len(disputed),
            "unverified_count": len(unverified)
        }

def assign_maturity_pool(
    product: dict,
    evidence_grade: str,
    hard_constraints_pass: bool = True
) -> str:
    """Assigns a product to one of the four distinct maturity pools:
    - excluded: Violates safety_compatibility_hard or user_declared_hard.
    - watch_list: Emerging product or severe unverified risk / high uncertainty.
    - conditional_recommendations: Solid performance but conditional on specific usage, short market tenure, or accessory needs.
    - mature_recommendations: Proven track record, broad applicability, stable batch history.
    """
    if not hard_constraints_pass or product.get("excluded", False):
        return "excluded"
        
    market_months = product.get("market_months", 12)
    has_long_term_durability_data = product.get("has_long_term_durability_data", True)
    
    if evidence_grade == "U":
        return "watch_list"
    elif evidence_grade == "B":
        # Disputed evidence -> watch list or conditional depending on severity
        return "watch_list" if product.get("critical_risk_disputed", False) else "conditional_recommendations"
        
    # S or A grade
    if market_months < 3 or not has_long_term_durability_data:
        # New product with strong short-term evidence is conditional
        return "conditional_recommendations"
    else:
        return "mature_recommendations"

if __name__ == "__main__":
    print("Evidence Confidence Engine ready.")
