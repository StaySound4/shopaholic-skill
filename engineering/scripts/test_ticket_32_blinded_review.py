#!/usr/bin/env python3
"""Test suite for Ticket 32: Create blinded human factual and usefulness adjudication.
Tests:
1. Pass: 10-pair pilot dataset verifies complete label blinding and dual-reviewer adjudication.
2. Adversarial: Order swap invariance verifies absence of position bias.
3. Adversarial: Sham control & non-fatal correctness tests verify presentation cannot override factual correctness.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blinded_human_adjudicator import (
    BlindedReviewPacket,
    evaluate_review_rubric,
    adjudicate_packet,
    calculate_inter_rater_agreement
)

class TestTicket32BlindedReview(unittest.TestCase):
    def test_01_pilot_10_pairs_blinding_and_adjudication(self):
        """Pass path: Run 10-pair pilot, verify condition labels are hidden and agreement is computed."""
        records = []
        for i in range(10):
            p = BlindedReviewPacket(
                case_id=f"PILOT-CASE-{i+1:02d}",
                prompt=f"Recommend a display under 3000 RMB #{i+1}",
                candidate_a_raw=f"Candidate A output #{i+1}",
                candidate_b_raw=f"Candidate B output #{i+1}",
                seed=100 + i
            )
            blinded = p.get_blinded_payload()
            # Ensure condition names are hidden
            self.assertIn("option_left", blinded)
            self.assertIn("option_right", blinded)
            self.assertNotIn("candidate_a_raw", blinded)
            self.assertNotIn("candidate_b_raw", blinded)
            
            # Reviewer 1 & 2 evaluations
            r1_eval = ({"factual_correctness": 1.0, "safety_score": 1.0, "usefulness": 0.9, "presentation": 0.8},
                       {"factual_correctness": 0.8, "safety_score": 0.8, "usefulness": 0.7, "presentation": 0.8})
            r2_eval = ({"factual_correctness": 1.0, "safety_score": 1.0, "usefulness": 0.9, "presentation": 0.8},
                       {"factual_correctness": 0.8, "safety_score": 0.8, "usefulness": 0.7, "presentation": 0.8})
            
            res = adjudicate_packet(p, r1_eval, r2_eval)
            records.append(res)
            
        agreement = calculate_inter_rater_agreement(records)
        self.assertEqual(agreement, 1.0)
        self.assertEqual(len(records), 10)

    def test_02_adversarial_position_swap_invariance(self):
        """Adversarial path: Swapping presentation order preserves unblinded winner origin."""
        # Force non-swapped packet
        p_normal = BlindedReviewPacket("CASE-SWAP", "prompt", "Better Candidate A", "Worse Candidate B", seed=42)
        p_normal.swapped = False
        p_normal.left_text = "Better Candidate A"; p_normal.left_origin = "candidate_a"
        p_normal.right_text = "Worse Candidate B"; p_normal.right_origin = "candidate_b"

        # Force swapped packet
        p_swapped = BlindedReviewPacket("CASE-SWAP", "prompt", "Better Candidate A", "Worse Candidate B", seed=42)
        p_swapped.swapped = True
        p_swapped.left_text = "Worse Candidate B"; p_swapped.left_origin = "candidate_b"
        p_swapped.right_text = "Better Candidate A"; p_swapped.right_origin = "candidate_a"

        # Reviewer grades Better Candidate with 1.0, Worse Candidate with 0.6
        res_normal = adjudicate_packet(
            p_normal,
            ({"factual_correctness": 1.0, "safety_score": 1.0}, {"factual_correctness": 0.6, "safety_score": 0.6}),
            ({"factual_correctness": 1.0, "safety_score": 1.0}, {"factual_correctness": 0.6, "safety_score": 0.6})
        )
        res_swapped = adjudicate_packet(
            p_swapped,
            ({"factual_correctness": 0.6, "safety_score": 0.6}, {"factual_correctness": 1.0, "safety_score": 1.0}),
            ({"factual_correctness": 0.6, "safety_score": 0.6}, {"factual_correctness": 1.0, "safety_score": 1.0})
        )

        self.assertEqual(res_normal["winner_origin"], "candidate_a")
        self.assertEqual(res_swapped["winner_origin"], "candidate_a")

    def test_03_adversarial_sham_and_correctness_priority_over_presentation(self):
        """Adversarial path: Gorgeous formatting cannot override factual correctness in fatal or non-fatal deltas."""
        # Fatal test
        score_fatal = {"factual_correctness": 0.0, "safety_score": 1.0, "presentation": 1.0}
        score_plain = {"factual_correctness": 1.0, "safety_score": 1.0, "presentation": 0.1}
        self.assertEqual(evaluate_review_rubric(score_fatal, score_plain), "right")

        # Non-fatal correctness superiority (1.0 vs 0.7) with inferior presentation (0.2 vs 1.0)
        score_better_facts = {"factual_correctness": 1.0, "safety_score": 1.0, "usefulness": 0.8, "presentation": 0.2}
        score_worse_facts = {"factual_correctness": 0.7, "safety_score": 0.7, "usefulness": 1.0, "presentation": 1.0}
        self.assertEqual(evaluate_review_rubric(score_better_facts, score_worse_facts), "left")

if __name__ == "__main__":
    unittest.main()
