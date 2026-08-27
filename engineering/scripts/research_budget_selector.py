#!/usr/bin/env python3
"""Research budget selection engine (R0-R3).
Selects appropriate research depth, candidate pool sizes, and verification rigor
based on safety/regulatory stakes, price/irreversibility, complexity, and installation risk.
"""
import argparse, json, sys
from pathlib import Path

# High safety-critical domain keywords that mandate R2 or R3 regardless of price
SAFETY_CRITICAL_DOMAINS = [
    "infant", "baby", "car_seat", "medical", "laser_eye", "climbing_gear", 
    "respirator", "water_purifier_membrane", "helmet", "fire_extinguisher"
]

def select_research_budget(
    category: str,
    price_cny: float,
    is_safety_critical: bool = False,
    is_built_in_or_installation_heavy: bool = False,
    has_high_ecosystem_lockin: bool = False,
    user_declared_urgency: str | None = None
) -> dict:
    """Selects research budget R0, R1, R2, or R3 with explicit reasoning."""
    cat_lower = category.lower()
    
    # 1. Check safety critical overrides -> R3 or R2
    safety_hit = is_safety_critical or any(k in cat_lower for k in SAFETY_CRITICAL_DOMAINS)
    if safety_hit:
        if "medical" in cat_lower or "laser" in cat_lower or "car_seat" in cat_lower:
            return {
                "research_budget": "R3",
                "reason": "[R3] Safety-critical / regulated medical / personal life safety domain requires authoritative regulatory registry verification and zero-tolerance safety screening.",
                "max_candidate_count": 3,
                "require_bom_teardown": True,
                "require_regulatory_registry_check": True
            }
        else:
            return {
                "research_budget": "R2",
                "reason": "[R2] Ingestion / infant / bodily contact safety stakes require thorough component and toxicology verification.",
                "max_candidate_count": 3,
                "require_bom_teardown": True,
                "require_regulatory_registry_check": True
            }
            
    # 2. Check high-price / high-irreversibility / installation-heavy -> R2
    if price_cny >= 10000 or is_built_in_or_installation_heavy or (price_cny >= 5000 and has_high_ecosystem_lockin):
        return {
            "research_budget": "R2",
            "reason": f"[R2] High value (CNY {price_cny}) or heavy physical installation/lock-in requires full provenance, revision history, and 4D cost-of-pivot analysis.",
            "max_candidate_count": 3,
            "require_bom_teardown": True,
            "require_regulatory_registry_check": True
        }
        
    # 3. Check low-cost, mature, highly reversible products -> R0
    # Price threshold: <= 150 CNY for mature accessories (chargers, cables, cases, mats)
    low_cost_accessories = ["charger", "cable", "case", "cover", "mat", "stand", "mouse_pad", "adapter_plug", "stylus_tip"]
    if price_cny <= 150 and any(k in cat_lower for k in low_cost_accessories):
        return {
            "research_budget": "R0",
            "reason": f"[R0] Low-cost (CNY {price_cny}), mature standard, highly reversible purchase: fast convergence with 2-4 candidates without heavy BOM teardown quotas.",
            "max_candidate_count": 4,
            "require_bom_teardown": False,
            "require_regulatory_registry_check": False
        }
        
    # 4. Standard consumer goods -> R1
    return {
        "research_budget": "R1",
        "reason": "[R1] Standard consumer durable: standard product entity resolution, primary spec verification, and Pareto trade-off analysis.",
        "max_candidate_count": 3,
        "require_bom_teardown": False,
        "require_regulatory_registry_check": True
    }

if __name__ == "__main__":
    print("Research Budget Selector Module ready.")
