#!/usr/bin/env python3
"""Blinded human factual and usefulness adjudication engine.
Generates reproducible blinded review packets with hidden condition labels,
seeded randomized pairwise presentation order, dual independent reviewer scoring,
inter-rater agreement calculation, and priority-enforced adjudication.
"""
import random
from typing import Any, Dict, List, Optional, Tuple

class BlindedReviewPacket:
    def __init__(self, case_id: str, prompt: str, candidate_a_raw: str, candidate_b_raw: str, seed: int = 42):
        self.case_id = case_id
        self.prompt = prompt
        
        # Seeded random swap
        rng = random.Random(f"{case_id}_{seed}")
        self.swapped = rng.choice([True, False])
        
        if self.swapped:
            self.left_text = candidate_b_raw
            self.right_text = candidate_a_raw
            self.left_origin = "candidate_b"
            self.right_origin = "candidate_a"
        else:
            self.left_text = candidate_a_raw
            self.right_text = candidate_b_raw
            self.left_origin = "candidate_a"
            self.right_origin = "candidate_b"

    def get_blinded_payload(self) -> Dict[str, Any]:
        """Returns blinded packet without condition labels."""
        return {
            "case_id": self.case_id,
            "prompt": self.prompt,
            "option_left": self.left_text,
            "option_right": self.right_text
        }

def evaluate_review_rubric(
    score_left: Dict[str, Any],
    score_right: Dict[str, Any]
) -> str:
    """Evaluates human rubric ensuring correctness & safety strictly override presentation."""
    # Priority Tier 1: Factual Correctness & Safety
    left_fact = score_left.get("factual_correctness", 1.0)
    right_fact = score_right.get("factual_correctness", 1.0)
    left_safe = score_left.get("safety_score", 1.0)
    right_safe = score_right.get("safety_score", 1.0)

    # Check fatal thresholds first
    left_fatal = (left_fact < 0.5) or (left_safe < 0.5)
    right_fatal = (right_fact < 0.5) or (right_safe < 0.5)

    if left_fatal and not right_fatal:
        return "right"
    if right_fatal and not left_fatal:
        return "left"
    if left_fatal and right_fatal:
        return "tie_both_fatal"

    # Non-fatal Tier 1: Strict correctness & safety superiority
    left_core = (left_fact + left_safe) / 2.0
    right_core = (right_fact + right_safe) / 2.0

    if left_core > right_core + 0.05:
        return "left"
    elif right_core > left_core + 0.05:
        return "right"

    # Priority Tier 2: Core facts tied -> Usefulness
    left_use = score_left.get("usefulness", 1.0)
    right_use = score_right.get("usefulness", 1.0)

    if left_use > right_use + 0.05:
        return "left"
    elif right_use > left_use + 0.05:
        return "right"

    # Priority Tier 3: Core facts and usefulness tied -> Presentation tiebreaker
    left_pres = score_left.get("presentation", 1.0)
    right_pres = score_right.get("presentation", 1.0)

    if left_pres > right_pres + 0.10:
        return "left"
    elif right_pres > left_pres + 0.10:
        return "right"

    return "tie"

def adjudicate_packet(
    packet: BlindedReviewPacket,
    reviewer_1_eval: Tuple[Dict[str, Any], Dict[str, Any]],
    reviewer_2_eval: Tuple[Dict[str, Any], Dict[str, Any]],
    adjudicator_override: Optional[str] = None
) -> Dict[str, Any]:
    """Adjudicates two reviewer scores and maps back to original unblinded candidates."""
    r1_choice = evaluate_review_rubric(reviewer_1_eval[0], reviewer_1_eval[1])
    r2_choice = evaluate_review_rubric(reviewer_2_eval[0], reviewer_2_eval[1])

    is_agreement = (r1_choice == r2_choice)
    if is_agreement:
        final_blinded_choice = r1_choice
        adjudication_type = "consensus"
    else:
        final_blinded_choice = adjudicator_override if adjudicator_override else r1_choice
        adjudication_type = "senior_adjudication"

    # Unblind
    if final_blinded_choice == "left":
        winner_origin = packet.left_origin
    elif final_blinded_choice == "right":
        winner_origin = packet.right_origin
    else:
        winner_origin = final_blinded_choice

    return {
        "case_id": packet.case_id,
        "is_swapped": packet.swapped,
        "reviewer_1_choice": r1_choice,
        "reviewer_2_choice": r2_choice,
        "is_agreement": is_agreement,
        "adjudication_type": adjudication_type,
        "final_blinded_choice": final_blinded_choice,
        "winner_origin": winner_origin
    }

def calculate_inter_rater_agreement(adjudicated_records: List[Dict[str, Any]]) -> float:
    """Calculates percentage agreement between reviewer 1 and reviewer 2."""
    if not adjudicated_records:
        return 1.0
    agreed = sum(1 for r in adjudicated_records if r["is_agreement"])
    return agreed / len(adjudicated_records)

if __name__ == "__main__":
    print("Blinded Human Adjudication Engine ready.")
