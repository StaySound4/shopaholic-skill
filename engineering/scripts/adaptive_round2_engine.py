#!/usr/bin/env python3
"""Search-informed and optional Round 2 clarification engine.
Asks only questions whose answers materially change candidate survivor sets or ranking.
Strictly forbids presentation/matrix format questions, enforces category-eligibility for
used-goods inquiries, and automatically skips Round 2 when initial research is sufficient.
"""
from typing import Any, Dict, List, Optional, Set

# Categories strictly ineligible for used/refurbished inquiries due to hygiene/safety/degradation
USED_INELIGIBLE_CATEGORIES = {
    "baby_car_seat", "car_seat", "baby_bottle", "infant_gear", "breast_pump",
    "in_ear_earphones", "mattress", "underwear", "helmet", "respirator",
    "water_purifier_filter", "medical_device", "contact_lenses"
}

# Categories eligible for used/discontinued flagship trade-offs when inspectable
USED_ELIGIBLE_CATEGORIES = {
    "camera_body", "camera_lens", "pro_audio_monitor", "audio_interface",
    "workstation_pc", "graphics_card", "mechanical_keyboard", "hifi_amplifier"
}

FORBIDDEN_FORMAT_KEYWORDS = [
    "matrix", "table", "layout", "format", "dual-track", "presentation", "card_view", "markdown_table"
]

def is_category_eligible_for_used(category: str) -> bool:
    """Checks if category permits used/refurbished inquiries."""
    cat_lower = category.lower()
    if any(k in cat_lower for k in USED_INELIGIBLE_CATEGORIES):
        return False
    if any(k in cat_lower for k in USED_ELIGIBLE_CATEGORIES):
        return True
    return False

def evaluate_round2_necessity(
    category: str,
    research_survivors: List[Dict[str, Any]],
    user_declared_preferences: Dict[str, Any],
    discovered_routes: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Determines whether Round 2 is necessary and formulates decision-critical questions."""
    # 1. Check if input and survivors already have clear dominant solution
    if len(research_survivors) <= 1:
        return {
            "skip_round_2": True,
            "questions": [],
            "reason": "Clear dominant candidate or single survivor: Round 2 skipped directly to delivery."
        }

    # 2. Check for material decision fork between survivors
    # Case A: Brand-new mid-tier vs high-value inspectable used flagship discovered at same price point
    has_used_flagship_discovery = any(c.get("condition") == "used" or c.get("is_discontinued_flagship") for c in research_survivors)
    
    questions = []
    if has_used_flagship_discovery and is_category_eligible_for_used(category):
        questions.append({
            "topic": "used_vs_new_tradeoff",
            "question": f"In {category}, would you consider an inspectable prior-generation flagship (e.g. higher optical grade) or strictly brand-new current-gen?",
            "decision_consequence": "Filters out discontinued flagships if user strictly requires brand-new warranty."
        })

    # Case B: Significant bifurcation in technical architecture (e.g. OLED vs Mini-LED)
    tech_routes = set(c.get("tech_route") for c in research_survivors if c.get("tech_route"))
    if len(tech_routes) > 1 and "tech_route_preference" not in user_declared_preferences:
        routes_desc = " vs ".join(sorted(list(tech_routes)))
        questions.append({
            "topic": "tech_architecture_fork",
            "question": f"Found two distinct performance routes ({routes_desc}). Do you prioritize absolute contrast in dark rooms or peak daylight brightness?",
            "decision_consequence": "Prunes one entire technical architecture from final recommendations."
        })

    if not questions:
        return {
            "skip_round_2": True,
            "questions": [],
            "reason": "No material bifurcation requiring user tie-breaking: Round 2 skipped directly to delivery."
        }

    return {
        "skip_round_2": False,
        "questions": questions[:2],
        "reason": f"Discovered {len(questions)} material decision forks requiring user preference."
    }

def validate_question_safety(question_text: str) -> bool:
    """Guards against format/layout questions in Round 2."""
    q_lower = question_text.lower()
    for forbidden in FORBIDDEN_FORMAT_KEYWORDS:
        if forbidden in q_lower:
            return False
    return True

if __name__ == "__main__":
    print("Adaptive Round 2 Engine Module ready.")
