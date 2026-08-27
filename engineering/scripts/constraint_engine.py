#!/usr/bin/env python3
"""Three-class constraint engine.
Implements safety_compatibility_hard, user_declared_hard, and soft_preference evaluation,
enforcing strict candidate exclusion in final delivery while allowing broad search headroom.
"""
import argparse, json, re, sys
from pathlib import Path

def classify_constraint(constraint_text: str, context_kind: str | None = None) -> str:
    """Classifies a constraint into one of the three canonical classes:
    1. safety_compatibility_hard: physical fit, voltage, safety/standards, recall, mandatory physical compatibility
    2. user_declared_hard: budget cap, brand exclusion, no-used, declared ecosystem dependency, purchase market
    3. soft_preference: color, aesthetic, lighter weight preference, silence preference, soft brand affinity
    """
    text_lower = constraint_text.lower().strip()
    
    # Soft preference indicators (e.g. "prefer", "would like", "nice to have")
    soft_indicators = ["prefer", "like", "nice to have", "wish", "aesthetic", "color", "lighter is better", "sound"]
    if any(text_lower.startswith(s) or f" {s}" in text_lower for s in ["prefer", "nice to have", "wish"]):
        # Unless it explicitly specifies hard budget or safety
        if not any(k in text_lower for k in ["max budget", "must", "mandatory", "220v", "voltage", "recall", "exclude brand"]):
            return "soft_preference"
            
    # Safety / Physical compatibility keywords
    safety_keywords = [
        "voltage", "220v", "110v", "safety", "fire", "recall", "certification", "3c", 
        "physical fit", "dimension", "mounting", "standard", "leak", "toxic", "bpa"
    ]
    if any(k in text_lower for k in safety_keywords):
        return "safety_compatibility_hard"
        
    # User declared hard keywords
    user_hard_keywords = [
        "budget", "max price", "no-used", "brand exclusion", 
        "exclude", "must support", "ecosystem", "homekit", "new only"
    ]
    if any(k in text_lower for k in user_hard_keywords) or re.search(r'\b(under|below)\s+\d{3,}', text_lower):
        return "user_declared_hard"
        
    # Soft preference keywords
    return "soft_preference"
def evaluate_candidate_constraints(
    candidate: dict,
    safety_hard: list[dict],
    user_hard: list[dict],
    soft_prefs: list[dict]
) -> dict:
    """Evaluates a single candidate against all constraint sets.
    Returns exclusion status, violated constraints with reasons and classes, and soft preference score.
    """
    excluded = False
    violations = []
    
    # 1. Check safety_compatibility_hard
    for sh in safety_hard:
        key = sh.get("key")
        expected = sh.get("expected")
        actual = candidate.get(key)
        
        # Example check: voltage match
        if key == "voltage_compatible" and actual is False:
            excluded = True
            violations.append({
                "constraint_class": "safety_compatibility_hard",
                "key": key,
                "reason": f"Physical/Safety voltage mismatch: requires {expected}, got {candidate.get('voltage')}"
            })
        elif key == "active_recall" and actual is True:
            excluded = True
            violations.append({
                "constraint_class": "safety_compatibility_hard",
                "key": key,
                "reason": f"Active official recall detected affecting model {candidate.get('model')}"
            })
            
    # 2. Check user_declared_hard
    for uh in user_hard:
        key = uh.get("key")
        if key == "max_budget":
            budget_cap = uh.get("value")
            price = candidate.get("price", 0)
            if price > budget_cap:
                excluded = True
                violations.append({
                    "constraint_class": "user_declared_hard",
                    "key": key,
                    "reason": f"Price {price} exceeds declared user budget cap {budget_cap}"
                })
        elif key == "excluded_brands":
            brand = candidate.get("brand", "").lower()
            ex_list = [b.lower() for b in uh.get("brands", [])]
            if brand in ex_list:
                excluded = True
                violations.append({
                    "constraint_class": "user_declared_hard",
                    "key": key,
                    "reason": f"Brand '{candidate.get('brand')}' is in user exclusion list"
                })
        elif key == "required_ecosystem":
            eco = uh.get("ecosystem")
            supported_ecos = candidate.get("supported_ecosystems", [])
            if eco not in supported_ecos:
                excluded = True
                violations.append({
                    "constraint_class": "user_declared_hard",
                    "key": key,
                    "reason": f"Product lacks mandatory user-declared ecosystem support for '{eco}'"
                })
        elif key == "no_used":
            condition = candidate.get("item_condition", "new")
            if condition != "new":
                excluded = True
                violations.append({
                    "constraint_class": "user_declared_hard",
                    "key": key,
                    "reason": f"Used/refurbished product '{condition}' violates user 'no-used' hard constraint"
                })

    # 3. Compute soft preference alignment (does NOT exclude)
    soft_score = 0.0
    matched_soft = []
    for sp in soft_prefs:
        key = sp.get("key")
        pref_val = sp.get("value")
        actual_val = candidate.get(key)
        if actual_val == pref_val:
            soft_score += 1.0
            matched_soft.append(key)
            
    return {
        "candidate_name": candidate.get("name"),
        "eligible_for_recommendation": not excluded,
        "excluded": excluded,
        "violations": violations,
        "soft_preference_score": soft_score,
        "matched_soft_preferences": matched_soft
    }

def process_candidate_pools(
    candidates: list[dict],
    constraints: dict,
    search_headroom_multiplier: float = 1.4
) -> dict:
    """Processes candidates into delivery pools with strict hard constraint exclusion,
    while separating broad search exploration candidates used for physics grounding.
    """
    safety_hard = constraints.get("safety_compatibility_hard", [])
    user_hard = constraints.get("user_declared_hard", [])
    soft_prefs = constraints.get("soft_preference", [])
    
    surviving_recommendations = []
    excluded_pool = []
    flagship_benchmarks_for_grounding = []
    
    budget_cap = None
    for uh in user_hard:
        if uh.get("key") == "max_budget":
            budget_cap = uh.get("value")
            
    for cand in candidates:
        eval_res = evaluate_candidate_constraints(cand, safety_hard, user_hard, soft_prefs)
        
        # Check if this was a search headroom benchmark
        if budget_cap and cand.get("price", 0) > budget_cap and cand.get("price", 0) <= budget_cap * search_headroom_multiplier:
            flagship_benchmarks_for_grounding.append({
                "candidate": cand.get("name"),
                "price": cand.get("price"),
                "role": "search_headroom_physics_benchmark",
                "grounding_insights": cand.get("physics_insights", "Benchmark for technical compromise attribution")
            })
            
        if eval_res["eligible_for_recommendation"]:
            surviving_recommendations.append({
                "candidate": cand,
                "evaluation": eval_res
            })
        else:
            excluded_pool.append({
                "candidate": cand,
                "evaluation": eval_res
            })
            
    # Sort surviving recommendations by soft preference score descending
    surviving_recommendations.sort(key=lambda x: x["evaluation"]["soft_preference_score"], reverse=True)
    
    return {
        "surviving_recommendations": [s["candidate"] for s in surviving_recommendations],
        "excluded_candidates": excluded_pool,
        "flagship_benchmarks_for_grounding": flagship_benchmarks_for_grounding,
        "constraint_summary": {
            "safety_hard_count": len(safety_hard),
            "user_hard_count": len(user_hard),
            "soft_pref_count": len(soft_prefs)
        }
    }

if __name__ == "__main__":
    print("Constraint Engine Module ready.")
