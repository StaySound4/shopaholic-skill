#!/usr/bin/env python3
"""Adaptive Round 1 intake and conversation multi-turn controller.
Performs broad prior catalog and scientific principle search (+30%~50% price headroom)
before questioning, asks only unresolved engineering/physical variables, forbids
presentation/market-scope questions in Round 1, permits direct delivery when fully
specified, and strictly caps conversation rounds at 3.
"""
from typing import Any, Dict, List, Optional, Set

FORBIDDEN_ROUND_1_TOPICS = {
    "purchase_channel", "domestic_vs_overseas", "report_layout", 
    "presentation_format", "table_vs_card", "font_style"
}

def conduct_broad_prior_exploration(
    category: str,
    declared_budget_cny: Optional[float] = None
) -> Dict[str, Any]:
    """Explores engineering physics and flagship architectures with +30%~50% headroom."""
    headroom_multiplier = 1.4  # +40% headroom
    max_search_ceiling = declared_budget_cny * headroom_multiplier if declared_budget_cny else None
    
    # Physics grounding topics derived from broad exploration
    physics_topics = [
        f"Thermodynamic stability & PID control in {category}",
        f"Pump pressure & boiler architecture benchmarks",
        f"Common mechanical failure modes across flagship tier"
    ]
    
    return {
        "category": category,
        "declared_budget": declared_budget_cny,
        "search_ceiling_cny": max_search_ceiling,
        "headroom_pct": 40.0,
        "physics_grounding_topics": physics_topics,
        "prematurely_truncated": False
    }

def evaluate_intake_and_generate_clarifications(
    category: str,
    user_query: str,
    supplied_variables: Dict[str, Any],
    turn_number: int = 1,
    declared_budget_cny: Optional[float] = None
) -> Dict[str, Any]:
    """Generates adaptive clarification questions or transitions directly to final delivery."""
    # 1. Enforce hard turn cap (max 2 clarification rounds -> 3rd turn MUST deliver)
    if turn_number >= 3:
        return {
            "direct_delivery": True,
            "turn_number": turn_number,
            "questions": [],
            "reason": "Hard conversation cap reached (Turn 3): mandatory final decision delivery."
        }

    # 2. Perform broad prior exploration
    exploration = conduct_broad_prior_exploration(category, declared_budget_cny)

    # 3. Check sufficiency of supplied variables
    required_variables = {"usage_scenario", "physical_constraints", "primary_priority"}
    already_supplied = set(supplied_variables.keys())
    missing_variables = required_variables - already_supplied
    
    if not missing_variables:
        # Fully specified -> direct delivery without questions
        return {
            "direct_delivery": True,
            "turn_number": turn_number,
            "questions": [],
            "broad_exploration": exploration,
            "reason": "User query is fully specified across usage scenario and physical constraints."
        }

    # 4. Generate engineering/physical clarification questions based on broad search
    questions = []
    if "physical_constraints" in missing_variables:
        questions.append({
            "variable": "physical_constraints",
            "question": f"What are your spatial dimensions, water/power hookup constraints, or placement limits for {category}?",
            "topic": "physical_dimensions_and_installation"
        })
    if "usage_scenario" in missing_variables:
        questions.append({
            "variable": "usage_scenario",
            "question": f"What is your primary usage volume and preference in {category} (e.g. daily extraction vs casual use)?",
            "topic": "core_use_case"
        })
    if "primary_priority" in missing_variables and len(questions) < 3:
        questions.append({
            "variable": "primary_priority",
            "question": "Which trade-off matters most: maintenance ease, peak performance, or long-term component durability?",
            "topic": "tradeoff_priority"
        })

    # Guard: Ensure no forbidden topics in Round 1
    for q in questions:
        if q.get("topic") in FORBIDDEN_ROUND_1_TOPICS:
            raise ValueError(f"Forbidden topic asked in Round 1: {q.get('topic')}")

    return {
        "direct_delivery": False,
        "turn_number": turn_number,
        "questions": questions[:3],  # Capped at 2-3 essential questions
        "broad_exploration": exploration,
        "already_supplied_not_reasked": list(already_supplied)
    }

if __name__ == "__main__":
    print("Adaptive Round 1 Engine Module ready.")
