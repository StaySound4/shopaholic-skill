#!/usr/bin/env python3
"""Deterministic sensitivity flip-point analysis engine.
Calculates exact linear preference weight thresholds that flip top candidate recommendations,
records input scores and normalization rules, translates mathematical thresholds into contextual
scenario sliders (e.g. usage split), articulates pairwise trade-off flip conditions for 2-way
and 3-way candidate rivalries, strictly suppresses sensitivity analysis under Pareto dominance,
and forbids ungrounded pseudo-probabilities.
"""
from typing import Any, Dict, List, Optional, Tuple

def compute_linear_flip_point(
    score_a_0: float,
    score_a_1: float,
    score_b_0: float,
    score_b_1: float
) -> Optional[float]:
    """Computes exact weight w_1 on Criterion 1 that equates A and B: (1-w)A0 + w A1 = (1-w)B0 + w B1."""
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
    criterion_1_label: Optional[str] = None,
    normalization_rule: str = "linear_0_to_100"
) -> Dict[str, Any]:
    """Performs deterministic sensitivity analysis between two close Pareto-frontier candidates."""
    name_a = candidate_a.get("name", "Candidate A")
    name_b = candidate_b.get("name", "Candidate B")
    
    a0 = float(candidate_a["scores"][criterion_0])
    a1 = float(candidate_a["scores"][criterion_1])
    b0 = float(candidate_b["scores"][criterion_0])
    b1 = float(candidate_b["scores"][criterion_1])
    
    input_metadata = {
        "candidate_a": {"name": name_a, "scores": {criterion_0: a0, criterion_1: a1}},
        "candidate_b": {"name": name_b, "scores": {criterion_0: b0, criterion_1: b1}},
        "normalization_rule": normalization_rule
    }

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
            "contextual_slider": None,
            "inputs_recorded": input_metadata
        }

    # 2. Compute exact deterministic flip point
    w_flip = compute_linear_flip_point(a0, a1, b0, b1)
    
    if w_flip is None:
        return {
            "suppressed": True,
            "suppression_reason": "No linear flip point exists within the valid weight interval [0.0, 1.0].",
            "flip_weight": None,
            "contextual_slider": None,
            "inputs_recorded": input_metadata
        }

    # 3. Format natural language contextual slider
    label0 = criterion_0_label or criterion_0
    label1 = criterion_1_label or criterion_1
    pct1 = round(w_flip * 100)
    pct0 = 100 - pct1
    
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
        },
        "inputs_recorded": input_metadata
    }

def analyze_three_candidate_rivalry(
    candidates: List[Dict[str, Any]],
    criterion_0: str,
    criterion_1: str,
    criterion_0_label: Optional[str] = None,
    criterion_1_label: Optional[str] = None
) -> Dict[str, Any]:
    """Articulates pairwise dominant trade-off flip conditions for 3-candidate rivalries."""
    if len(candidates) != 3:
        raise ValueError("analyze_three_candidate_rivalry requires exactly 3 candidates.")

    pairs = [
        (candidates[0], candidates[1]),
        (candidates[1], candidates[2]),
        (candidates[0], candidates[2])
    ]
    
    pairwise_analyses = []
    for c_i, c_j in pairs:
        res = analyze_candidate_sensitivity(
            candidate_a=c_i,
            candidate_b=c_j,
            criterion_0=criterion_0,
            criterion_1=criterion_1,
            criterion_0_label=criterion_0_label,
            criterion_1_label=criterion_1_label
        )
        pairwise_analyses.append({
            "pair": f"{c_i.get('name')} vs {c_j.get('name')}",
            "analysis": res
        })

    return {
        "rivalry_type": "three_candidate_pairwise_tradeoffs",
        "candidate_names": [c.get("name") for c in candidates],
        "pairwise_analyses": pairwise_analyses
    }

if __name__ == "__main__":
    print("Sensitivity Engine Module ready.")
