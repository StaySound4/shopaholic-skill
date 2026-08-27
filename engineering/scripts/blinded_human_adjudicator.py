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
    # Correctness & Safety check first
    left_fatal = (score_left.get("factual_correctness", 1.0) < 0.5) or (score_left.get("safety_score", 1.0) < 0.5)
    right_fatal = (score_right.get("factual_correctness", 1.0) < 0.5) or (score_right.get("safety_score", 1.0) < 0.5)

    if left_fatal and not right_fatal:
        return "right"
    if right_fatal and not left_fatal:
        return "left"
    if left_fatal and right_fatal:
        return "tie_both_fatal"

    # Both factual/safe -> Use weighted composite (correctness: 0.5, usefulness: 0.3, presentation: 0.2)
    left_composite = (
        0.5 * score_left.get("factual_correctness", 1.0) +
        0.3 * score_left.get("usefulness", 1.0) +
        0.2 * score_left.get("presentation", 1.0)
    )
    right_composite = (
        0.5 * score_right.get("factual_correctness", 1.0) +
        0.3 * score_right.get("usefulness", 1.0) +
        0.2 * score_right.get("presentation", 1.0)
    )

    if left_composite > right_composite + 0.05:
        return "left"
    elif right_composite > left_composite + 0.05:
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
