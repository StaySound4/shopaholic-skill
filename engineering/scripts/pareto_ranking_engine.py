#!/usr/bin/env python3
"""Pareto-first ranking and explicit preference weighting engine.
Eliminates hard constraint failures first, identifies and removes Pareto-dominated
options before applying any weighted scoring, and enforces transparent, inspectable
weight disclosures without silently inventing precise decimal weights from vague user prompts.
"""
from typing import Any, Dict, List, Optional, Tuple

class CandidateOption:
    def __init__(
        self,
        candidate_id: str,
        name: str,
        dimension_scores: Dict[str, float],   # Dimension name -> normalized score [0.0, 100.0]
        hard_constraint_passed: bool = True,
        hard_constraint_failure_reason: Optional[str] = None
    ):
        self.candidate_id = candidate_id
        self.name = name
        self.dimension_scores = dimension_scores
        self.hard_constraint_passed = hard_constraint_passed
        self.hard_constraint_failure_reason = hard_constraint_failure_reason
        self.is_dominated = False
        self.dominated_by: List[str] = []
        self.weighted_score: Optional[float] = None

def check_pareto_dominance(c_a: CandidateOption, c_b: CandidateOption, dimensions: List[str]) -> Tuple[bool, bool]:
    """Returns (a_dominates_b, b_dominates_a) based on evaluated dimensions."""
    a_better_or_equal = True
    a_strictly_better = False
    b_better_or_equal = True
    b_strictly_better = False

    for dim in dimensions:
        score_a = c_a.dimension_scores.get(dim, 0.0)
        score_b = c_b.dimension_scores.get(dim, 0.0)

        if score_a < score_b:
            a_better_or_equal = False
        if score_a > score_b:
            a_strictly_better = True

        if score_b < score_a:
            b_better_or_equal = False
        if score_b > score_a:
            b_strictly_better = True

    a_dominates_b = a_better_or_equal and a_strictly_better
    b_dominates_a = b_better_or_equal and b_strictly_better
    return a_dominates_b, b_dominates_a

def derive_preference_weights(
    qualitative_preferences: Dict[str, str],
    evaluated_dimensions: List[str]
) -> Dict[str, Any]:
    """Derives inspectable preference weights from user input with explicit tiers."""
    # Enforce discrete inspectable weight tiers instead of opaque invented decimals
    TIER_WEIGHTS = {
        "primary_focus": 0.6,
        "secondary_focus": 0.3,
        "standard_baseline": 0.1
    }
    
    weights = {}
    explanations = []
    
    # Check if user stated specific emphasis
    focus_dim = qualitative_preferences.get("stated_priority")
    if focus_dim and focus_dim in evaluated_dimensions:
        remaining_dims = [d for d in evaluated_dimensions if d != focus_dim]
        weights[focus_dim] = TIER_WEIGHTS["primary_focus"]
        explanations.append(f"Primary focus tier ({TIER_WEIGHTS['primary_focus']}) assigned to '{focus_dim}' based on stated preference.")
        
        rem_weight = round((1.0 - TIER_WEIGHTS["primary_focus"]) / max(1, len(remaining_dims)), 4)
        for d in remaining_dims:
            weights[d] = rem_weight
            explanations.append(f"Baseline tier ({rem_weight}) assigned to remaining dimension '{d}'.")
    else:
        # Equal weighting default
        eq_weight = round(1.0 / len(evaluated_dimensions), 4)
        for d in evaluated_dimensions:
            weights[d] = eq_weight
        explanations.append(f"Uniform default weighting ({eq_weight}) applied across all {len(evaluated_dimensions)} dimensions.")

    return {
        "weights": weights,
        "is_inspectable": True,
        "derivation_explanations": explanations,
        "silent_invented_decimals": False
    }

def rank_candidates_pareto_first(
    candidates: List[CandidateOption],
    evaluated_dimensions: List[str],
    qualitative_preferences: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Executes 3-stage ranking: Hard filter -> Pareto frontier -> Inspectable weighted ranking."""
    # Stage 1: Filter hard ineligible candidates
    eligible: List[CandidateOption] = []
    hard_rejected: List[CandidateOption] = []
    
    for c in candidates:
        if c.hard_constraint_passed:
            eligible.append(c)
        else:
            hard_rejected.append(c)

    # Stage 2: Pareto dominance identification among eligible candidates
    for i, c_i in enumerate(eligible):
        for j, c_j in enumerate(eligible):
            if i != j:
                c_i_dominates_j, _ = check_pareto_dominance(c_i, c_j, evaluated_dimensions)
                if c_i_dominates_j:
                    c_j.is_dominated = True
                    if c_i.candidate_id not in c_j.dominated_by:
                        c_j.dominated_by.append(c_i.candidate_id)

    pareto_frontier = [c for c in eligible if not c.is_dominated]
    pareto_dominated = [c for c in eligible if c.is_dominated]

    # Stage 3: Weighted ranking on Pareto frontier candidates
    weight_info = derive_preference_weights(qualitative_preferences or {}, evaluated_dimensions)
    weights = weight_info["weights"]

    for c in eligible:
        w_score = sum(c.dimension_scores.get(dim, 0.0) * weights.get(dim, 0.0) for dim in evaluated_dimensions)
        c.weighted_score = round(w_score, 2)

    # Top choices MUST come exclusively from Pareto frontier
    pareto_frontier_sorted = sorted(pareto_frontier, key=lambda x: x.weighted_score or 0.0, reverse=True)
    dominated_sorted = sorted(pareto_dominated, key=lambda x: x.weighted_score or 0.0, reverse=True)

    return {
        "top_recommendations": [
            {"candidate_id": c.candidate_id, "name": c.name, "score": c.weighted_score, "is_pareto_frontier": True}
            for c in pareto_frontier_sorted
        ],
        "pareto_dominated_candidates": [
            {"candidate_id": c.candidate_id, "name": c.name, "dominated_by": c.dominated_by, "score": c.weighted_score}
            for c in dominated_sorted
        ],
        "hard_rejected_candidates": [
            {"candidate_id": c.candidate_id, "name": c.name, "reason": c.hard_constraint_failure_reason}
            for c in hard_rejected
        ],
        "weight_disclosure": weight_info
    }

if __name__ == "__main__":
    print("Pareto Ranking Engine Module ready.")
