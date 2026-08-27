#!/usr/bin/env python3
"""Deterministic sensitivity flip-point analysis engine.
Calculates exact linear preference weight thresholds that flip top candidate recommendations,
translates mathematical thresholds into contextual scenario sliders (e.g. usage split),
articulates pairwise trade-off flip conditions for candidate rivalries, strictly suppresses
sensitivity analysis under Pareto dominance, and forbids ungrounded pseudo-probabilities.
"""
from typing import Any, Dict, List, Optional, Tuple

def compute_linear_flip_point(
    score_a_0: float,
    score_a_1: float,
    score_b_0: float,
    score_b_1: float
) -> Optional[float]:
    """Computes exact weight w_1 on Criterion 1 that equates A and B: (1-w)A0 + w A1 = (1-w)B0 + w B1."""
    # (1-w)(A0 - B0) = w(B1 - A1)
    # delta_0 * (1-w) = delta_1 * w
    # delta_0 = w * (delta_0 + delta_1)
    # w = delta_0 / (delta_0 + delta_1) = (B0 - A0) / ((A1 - A0) - (B1 - B0))
    numerator = score_b_0 - score_a_0
    denominator = (score_a_1 - score_a_0) - (score_b_1 - score_b_0)
    
    if abs(denominator) < 1e-12:
        return None
        
    w = numerator / denominator
    if 0.0 <= w <= 1.0:
        return round(w, 4)
    return None

def analyze_candidate_sensitivity(
    candidate_a: Dict[str, Any],
    candidate_b: Dict[str, Any],
    criterion_0: str,
    criterion_1: str,
    criterion_0_label: Optional[str] = None,
    criterion_1_label: Optional[str] = None
) -> Dict[str, Any]:
    """Performs deterministic sensitivity analysis between two close Pareto-frontier candidates."""
    name_a = candidate_a.get("name", "Candidate A")
    name_b = candidate_b.get("name", "Candidate B")
    
    a0 = float(candidate_a["scores"][criterion_0])
    a1 = float(candidate_a["scores"][criterion_1])
    b0 = float(candidate_b["scores"][criterion_0])
    b1 = float(candidate_b["scores"][criterion_1])
    
    # 1. Check Pareto dominance -> Strict suppression
    a_dominates_b = (a0 >= b0 and a1 >= b1) and (a0 > b0 or a1 > b1)
    b_dominates_a = (b0 >= a0 and b1 >= a1) and (b0 > a0 or b1 > a1)
    
    if a_dominates_b or b_dominates_a:
        dominator = name_a if a_dominates_b else name_b
        dominated = name_b if a_dominates_b else name_a
        return {
            "suppressed": True,
            "suppression_reason": f"Pareto dominance: {dominator} strictly dominates {dominated} across all evaluated criteria; no valid trade-off flip point exists.",
            "flip_weight": None,
            "contextual_slider": None
        }

    # 2. Compute exact deterministic flip point
    w_flip = compute_linear_flip_point(a0, a1, b0, b1)
    
    if w_flip is None:
        return {
            "suppressed": True,
            "suppression_reason": "No linear flip point exists within the valid weight interval [0.0, 1.0].",
            "flip_weight": None,
            "contextual_slider": None
        }

    # 3. Format natural language contextual slider
    label0 = criterion_0_label or criterion_0
    label1 = criterion_1_label or criterion_1
    pct1 = round(w_flip * 100)
    pct0 = 100 - pct1
    
    # Determine who wins on criterion 0 vs criterion 1
    winner_crit0 = name_a if a0 > b0 else name_b
    winner_crit1 = name_a if a1 > b1 else name_b
    
    slider_text = (
        f"Sensitivity Flip Slider: When {label0} priority >= {pct0}%, {winner_crit0} is the optimal choice; "
        f"when {label1} priority exceeds {pct1}%, recommendation flips decisively to {winner_crit1}."
    )

    return {
        "suppressed": False,
        "criterion_0": criterion_0,
        "criterion_1": criterion_1,
        "flip_weight_criterion_1": w_flip,
        "flip_weight_criterion_0": round(1.0 - w_flip, 4),
        "contextual_slider": slider_text,
        "pairwise_tradeoff": {
            "advantage_crit0": {"winner": winner_crit0, "margin": round(abs(a0 - b0), 2)},
            "advantage_crit1": {"winner": winner_crit1, "margin": round(abs(a1 - b1), 2)}
        }
    }

if __name__ == "__main__":
    print("Sensitivity Engine Module ready.")
