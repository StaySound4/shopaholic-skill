#!/usr/bin/env python3
"""Conditional cost-of-pivot (4D transfer cost) analysis engine.
Detects meaningful form-factor, mount, and technical architecture pivots,
populates relevant dimensions in structured pivot_cost records (workflow friction,
kinetic/ergonomic safety, compute/ecosystem, fragility/TCO), and suppresses analysis
for minor cosmetic/color variations.
"""
from typing import Any, Dict, List, Optional

# Known meaningful architectural pivot transitions
ARCHITECTURAL_PIVOT_DEFINITIONS = {
    ("standard_action_camera", "360_panoramic_camera"): {
        "pivot_name": "Standard Action Cam to 360 Panoramic Cam Pivot",
        "workflow_friction": "Requires compulsory dual-lens video stitching, reframing, and keyframing in post-production.",
        "kinetic_ergonomic_safety": "Exposed bulging fisheye lenses cannot use flat protective filters; vehicle roof suction mount requires tether safety wire.",
        "compute_ecosystem": "5.7K/8K 360 video editing demands high GPU VRAM and fast SSD storage.",
        "fragility_tco": "Unprotected dual optical elements have high accidental drop replacement cost; requires specialized lens guards."
    },
    ("traditional_air_cooling", "custom_open_loop_liquid"): {
        "pivot_name": "Air Cooling to Open-Loop Liquid Cooling Pivot",
        "workflow_friction": "Requires regular coolant flush, biocides maintenance, and loop pressure testing every 6-12 months.",
        "kinetic_ergonomic_safety": "Catastrophic liquid leakage risk over high-voltage motherboard and GPU VRM.",
        "compute_ecosystem": None, # Omitted as irrelevant
        "fragility_tco": "High initial block/fitting investment and risk of galvanic corrosion if metals mismatch."
    }
}

COSMETIC_ATTRIBUTE_KEYS = {"color", "finish", "cosmetic_edition", "box_art", "cable_braiding_color"}

def evaluate_cost_of_pivot(
    baseline_architecture: str,
    target_architecture: str,
    baseline_attributes: Optional[Dict[str, Any]] = None,
    target_attributes: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Evaluates whether an architectural pivot occurred and generates structured pivot cost record."""
    b_attrs = baseline_attributes or {}
    t_attrs = target_attributes or {}
    
    # 1. Check if change is solely cosmetic (e.g. black -> white color swap)
    if baseline_architecture == target_architecture:
        diff_keys = set(k for k in set(b_attrs.keys()).union(set(t_attrs.keys())) if b_attrs.get(k) != t_attrs.get(k))
        is_only_cosmetic = diff_keys.issubset(COSMETIC_ATTRIBUTE_KEYS) or len(diff_keys) == 0
        if is_only_cosmetic:
            return {
                "pivot_triggered": False,
                "reason": "Minor cosmetic/preference variation with unchanged underlying architecture: cost-of-pivot analysis suppressed.",
                "pivot_cost": None
            }

    # 2. Check for known architectural pivot transition
    transition_key = (baseline_architecture.lower(), target_architecture.lower())
    pivot_def = ARCHITECTURAL_PIVOT_DEFINITIONS.get(transition_key)
    
    if pivot_def:
        # Populate only relevant non-None dimensions
        populated_dimensions = {}
        for dim in ["workflow_friction", "kinetic_ergonomic_safety", "compute_ecosystem", "fragility_tco"]:
            val = pivot_def.get(dim)
            if val:
                populated_dimensions[dim] = val

        return {
            "pivot_triggered": True,
            "pivot_name": pivot_def["pivot_name"],
            "baseline_architecture": baseline_architecture,
            "target_architecture": target_architecture,
            "dimension_count": len(populated_dimensions),
            "pivot_cost": populated_dimensions
        }

    # 3. Generic architectural change
    if baseline_architecture != target_architecture:
        return {
            "pivot_triggered": True,
            "pivot_name": f"Architecture shift: {baseline_architecture} -> {target_architecture}",
            "baseline_architecture": baseline_architecture,
            "target_architecture": target_architecture,
            "dimension_count": 1,
            "pivot_cost": {
                "workflow_friction": f"Altered operating principles between {baseline_architecture} and {target_architecture} require learning curve."
            }
        }

    return {
        "pivot_triggered": False,
        "reason": "Identical architecture without significant workflow shift.",
        "pivot_cost": None
    }

if __name__ == "__main__":
    print("Pivot Cost Engine Module ready.")
