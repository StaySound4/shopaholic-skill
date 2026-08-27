#!/usr/bin/env python3
"""Legacy taxonomy and quota contraction engine.
Eradicates universal L1-L4 rankings and normative 8/10 source / 10-15 candidate quotas.
Decouples S/A/B/U evidence confidence from product maturity, migrating legacy
tier_a_mature / tier_b_observation structures into 4 explicit candidate pools:
mature_recommendations, conditional_recommendations, watch_list, and excluded.
Audits structured decision records against legacy terminology leakage.
"""
from typing import Any, Dict, List, Optional, Set

FORBIDDEN_LEGACY_FIELDS = {
    "tier_a_mature",
    "tier_b_observation",
    "l1_l4_truth_ranking",
    "l1_source_quota",
    "fixed_candidate_quota"
}

VALID_EXPLICIT_POOLS = {
    "mature_recommendations",
    "conditional_recommendations",
    "watch_list",
    "excluded"
}

def migrate_legacy_candidate_pools(legacy_pools_dict: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Migrates legacy candidate_pools payload to 4 canonical explicit pools."""
    migrated: Dict[str, List[Dict[str, Any]]] = {
        "mature_recommendations": [],
        "conditional_recommendations": [],
        "watch_list": [],
        "excluded": []
    }
    
    # 1. Migrate legacy tier_a_mature -> mature_recommendations
    if "tier_a_mature" in legacy_pools_dict:
        migrated["mature_recommendations"].extend(legacy_pools_dict["tier_a_mature"])
        
    # 2. Migrate legacy tier_b_observation -> watch_list / conditional_recommendations
    if "tier_b_observation" in legacy_pools_dict:
        for cand in legacy_pools_dict["tier_b_observation"]:
            # If candidate is a conditional/discontinued flagship, route to conditional_recommendations
            if cand.get("condition") == "used" or cand.get("is_conditional"):
                migrated["conditional_recommendations"].append(cand)
            else:
                migrated["watch_list"].append(cand)

    # 3. Adopt canonical pools if already present
    for pool in VALID_EXPLICIT_POOLS:
        if pool in legacy_pools_dict and pool not in ["mature_recommendations", "conditional_recommendations", "watch_list"]:
            migrated[pool].extend(legacy_pools_dict[pool])
        elif pool in legacy_pools_dict and not legacy_pools_dict.get("tier_a_mature"):
            migrated[pool] = legacy_pools_dict[pool]

    return migrated

def audit_record_for_legacy_leakage(record: Dict[str, Any]) -> Dict[str, Any]:
    """Audits structured record for legacy L1-L4 or quota terminology."""
    violations = []
    
    def check_dict(d: Any, path: str = ""):
        if isinstance(d, dict):
            for k, v in d.items():
                curr_path = f"{path}.{k}" if path else k
                if k.lower() in FORBIDDEN_LEGACY_FIELDS:
                    violations.append(f"Forbidden legacy field found: '{curr_path}'")
                if "l1_l4" in k.lower() or "tier_a" in k.lower():
                    violations.append(f"Forbidden legacy naming found in key: '{curr_path}'")
                check_dict(v, curr_path)
        elif isinstance(d, list):
            for i, elem in enumerate(d):
                check_dict(elem, f"{path}[{i}]")

    check_dict(record)
    
    # Verify candidate_pools format if present
    candidate_pools = record.get("candidate_pools")
    if candidate_pools:
        for pool_key in candidate_pools.keys():
            if pool_key not in VALID_EXPLICIT_POOLS:
                violations.append(f"Invalid non-canonical candidate pool key: '{pool_key}'")

    return {
        "is_clean": len(violations) == 0,
        "violation_count": len(violations),
        "violations": violations
    }

if __name__ == "__main__":
    print("Legacy Contract Migrator Module ready.")
