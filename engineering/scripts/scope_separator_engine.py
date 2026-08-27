#!/usr/bin/env python3
"""Scope separation and global evidence cross-verification engine.
Independently maintains evidence_scope, purchase_scope, and output_scope.
Allows global regulatory / laboratory registries (FCC, EPREL, VESA, FDA, TÜV)
to verify product claims and expose component downgrades without leaking overseas
purchase candidates into China-only purchase requests.
"""
from typing import Any, Dict, List, Optional

VALID_EVIDENCE_SCOPES = {"global", "cn_only", "overseas_only"}
VALID_PURCHASE_SCOPES = {"cn", "overseas", "both"}
VALID_OUTPUT_SCOPES = {"cn", "overseas", "combined"}

class ScopeContext:
    def __init__(
        self,
        purchase_scope: str = "cn",
        output_scope: str = "cn",
        evidence_scope: str = "global"
    ):
        if purchase_scope not in VALID_PURCHASE_SCOPES:
            raise ValueError(f"Invalid purchase_scope: {purchase_scope}")
        if output_scope not in VALID_OUTPUT_SCOPES:
            raise ValueError(f"Invalid output_scope: {output_scope}")
        if evidence_scope not in VALID_EVIDENCE_SCOPES:
            raise ValueError(f"Invalid evidence_scope: {evidence_scope}")

        self.purchase_scope = purchase_scope
        self.output_scope = output_scope
        self.evidence_scope = evidence_scope

    def filter_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters candidate products strictly by purchase_scope."""
        filtered = []
        for cand in candidates:
            market_availability = cand.get("market_availability", ["cn"])
            if self.purchase_scope == "cn" and "cn" in market_availability:
                filtered.append(cand)
            elif self.purchase_scope == "overseas" and "overseas" in market_availability:
                filtered.append(cand)
            elif self.purchase_scope == "both":
                filtered.append(cand)
        return filtered

def cross_verify_with_global_evidence(
    domestic_claim: Dict[str, Any],
    global_registry_evidence: Optional[Dict[str, Any]] = None,
    fcc_or_teardown_evidence: Optional[Dict[str, Any]] = None,
    scope_context: Optional[ScopeContext] = None
) -> Dict[str, Any]:
    """Cross-verifies domestic claims against global registry/teardown evidence."""
    ctx = scope_context or ScopeContext()
    
    claim_name = domestic_claim.get("claim_name")
    claimed_value = domestic_claim.get("claimed_value")
    
    result = {
        "claim_name": claim_name,
        "claimed_value": claimed_value,
        "evidence_scope": ctx.evidence_scope,
        "purchase_scope": ctx.purchase_scope,
        "status": "unverified",
        "cmd_discrepancy_detected": False,
        "notes": ""
    }
    
    # 1. Check certification registry (e.g. VESA DisplayHDR, EPREL)
    if global_registry_evidence:
        certified_status = global_registry_evidence.get("certified", False)
        certified_tier = global_registry_evidence.get("certified_tier")
        if not certified_status:
            result["status"] = "disputed"
            result["cmd_discrepancy_detected"] = True
            result["notes"] = f"Claimed '{claimed_value}' not found in official global registry."
        elif certified_tier and certified_tier != claimed_value:
            result["status"] = "disputed"
            result["cmd_discrepancy_detected"] = True
            result["notes"] = f"Claimed '{claimed_value}', but global registry certifies lower tier '{certified_tier}'."
        else:
            result["status"] = "verified"
            result["notes"] = f"Verified in global registry as '{certified_tier or claimed_value}'."

    # 2. Check internal teardown / FCC ID filings for component downgrades
    if fcc_or_teardown_evidence:
        overseas_spec = fcc_or_teardown_evidence.get("global_sku_spec")
        domestic_spec = fcc_or_teardown_evidence.get("domestic_sku_spec")
        if overseas_spec and domestic_spec and overseas_spec != domestic_spec:
            result["cmd_discrepancy_detected"] = True
            result["status"] = "disputed"
            result["notes"] += f" Component downgrade detected: Global SKU has {overseas_spec}, while Domestic SKU has {domestic_spec}."

    return result

if __name__ == "__main__":
    print("Scope Separator Engine Module ready.")
