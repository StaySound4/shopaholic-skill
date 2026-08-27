#!/usr/bin/env python3
"""Category-aware used and discontinued products evaluation engine.
Evaluates used/discontinued eligibility based on hidden-history risk, safety, hygiene,
support/EOL lifecycle, battery degradation, device lockouts, and physical inspectability.
Generates strict category-specific inspection checklists and prevents cross-category checklist leakage.
"""
from typing import Any, Dict, List, Optional

CATEGORY_CHECKLISTS = {
    "camera_body": [
        "CMOS sensor hot pixel / dead pixel scan at base ISO and high ISO",
        "Mechanical shutter actuation count verification vs rated lifespan",
        "Sensor IBIS (In-Body Image Stabilization) mechanical axis centering",
        "Lens mount electronic contact wear and physical flatness",
        "Battery bay contact integrity and OEM battery swelling check"
    ],
    "camera_lens": [
        "Internal optical glass inspection for fungus, haze, separation, or scratch",
        "Aperture blade responsiveness and oil contamination check",
        "Linear / stepping autofocus motor smooth operation and noise check",
        "Optical axis decentering / tilt test against planar chart"
    ],
    "laptop_workstation": [
        "OEM battery health capacity percentage and cycle count",
        "BIOS / UEFI administrator password and MDM enterprise enrollment lock check",
        "Motherboard liquid damage contact indicator inspection",
        "Display panel backlight bleed, dead pixels, and uniform luminance check",
        "SSD total bytes written (TBW) and SMART health status"
    ],
    "espresso_machine": [
        "Boiler scale buildup inspection and descaling history",
        "Group head brass collar wear and 3-way solenoid valve drainage",
        "Vibration / rotary pump pressure stability under 9-bar blind basket test",
        "Steam wand valve seal and thermal element insulation resistance"
    ]
}

SAFETY_CRITICAL_RESTRICTED_CATEGORIES = {
    "baby_car_seat": "Hidden internal EPS/EPP energy-absorption micro-cracks from undocumented vehicle collision history cannot be verified non-destructively.",
    "climbing_rope": "Internal core fiber degradation from unseen dynamic falls or chemical exposure poses catastrophic life-safety hazard.",
    "motorcycle_helmet": "Single-impact EPS liner compression renders helmet structurally compromised even if exterior shell appears pristine."
}

def evaluate_used_product_eligibility(
    category: str,
    product_model: str,
    release_year: Optional[int] = None,
    current_year: int = 2026,
    eol_support_status: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Evaluates used eligibility, safety restrictions, EOL trade-offs, and generates category-specific checklist."""
    cat_lower = category.lower()
    
    # 1. Check safety-critical hidden-history restrictions
    for restricted_cat, risk_rationale in SAFETY_CRITICAL_RESTRICTED_CATEGORIES.items():
        if restricted_cat in cat_lower:
            return {
                "category": category,
                "product_model": product_model,
                "eligibility": "restricted_safety_hazard",
                "recommended_for_used": False,
                "safety_restriction_rationale": risk_rationale,
                "checklist": [],
                "eol_tradeoff": None
            }

    # 2. Check category-specific inspection checklist
    checklist = []
    matched_checklist_key = None
    for key, items in CATEGORY_CHECKLISTS.items():
        if key in cat_lower:
            checklist = items
            matched_checklist_key = key
            break

    # 3. Check EOL / Support / Consumables lifecycle
    eol_tradeoff = None
    if release_year:
        age_years = current_year - release_year
        if age_years >= 5:
            eol_tradeoff = {
                "age_years": age_years,
                "driver_os_compatibility_warning": eol_support_status.get("driver_support", "Legacy OS only") if eol_support_status else "Verify current OS driver & security patch availability.",
                "consumable_availability": eol_support_status.get("consumable_status", "Requires checking third-party supply chain") if eol_support_status else "OEM parts may be discontinued."
            }

    is_eligible = bool(checklist)
    return {
        "category": category,
        "product_model": product_model,
        "eligibility": "admissible" if is_eligible else "unsupported_category",
        "recommended_for_used": is_eligible,
        "matched_category": matched_checklist_key,
        "checklist": checklist,
        "eol_tradeoff": eol_tradeoff
    }

if __name__ == "__main__":
    print("Used Goods Evaluator Module ready.")
