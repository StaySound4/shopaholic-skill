#!/usr/bin/env python3
"""Test suite for Ticket 24: Use Pareto-first ranking and explicit preference weights.
Tests:
1. Pass: Hard-ineligible candidate never returns through high soft scores.
2. Pass: Pareto-dominated candidate (worse on all evaluated dimensions) is flagged and removed from top recommendations.
3. Pass: Preference weights are inspectable with transparent tier justifications.
4. Adversarial: '比较看重视频' prompt derives transparent discrete tier weight, strictly avoiding silent invented decimal weights.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pareto_ranking_engine import (
    CandidateOption,
    rank_candidates_pareto_first,
    derive_preference_weights
)

class TestTicket24Pareto(unittest.TestCase):
    def test_01_hard_ineligible_never_resurrects_from_high_score(self):
        """Pass path: Product failing hard safety limits cannot enter recommendations even with 100 score."""
        c_unsafe = CandidateOption(
            candidate_id="UNSAFE-001",
            name="Super Fast but Toxic Kettle",
            dimension_scores={"boiling_speed": 100.0, "thermal_efficiency": 100.0},
            hard_constraint_passed=False,
            hard_constraint_failure_reason="Failed GB 4806 heavy metal leaching test."
        )
        c_safe = CandidateOption(
            candidate_id="SAFE-002",
            name="Standard Compliant Kettle",
            dimension_scores={"boiling_speed": 80.0, "thermal_efficiency": 85.0},
            hard_constraint_passed=True
        )
        
        res = rank_candidates_pareto_first(
            candidates=[c_unsafe, c_safe],
            evaluated_dimensions=["boiling_speed", "thermal_efficiency"]
        )
        top_ids = [c["candidate_id"] for c in res["top_recommendations"]]
        self.assertNotIn("UNSAFE-001", top_ids)
        self.assertIn("SAFE-002", top_ids)
        self.assertEqual(len(res["hard_rejected_candidates"]), 1)

    def test_02_pareto_dominated_candidate_removed_from_top_picks(self):
        """Pass path: Candidate C strictly dominated by Candidate A on all dimensions cannot win."""
        # A: (video: 90, photo: 85)
        # B: (video: 70, photo: 95) -> Non-dominated tradeoff
        # C: (video: 60, photo: 70) -> Strictly dominated by A
        c_a = CandidateOption("CAM-A", "Camera A", {"video": 90.0, "photo": 85.0})
        c_b = CandidateOption("CAM-B", "Camera B", {"video": 70.0, "photo": 95.0})
        c_c = CandidateOption("CAM-C", "Camera C", {"video": 60.0, "photo": 70.0})

        res = rank_candidates_pareto_first(
            candidates=[c_a, c_b, c_c],
            evaluated_dimensions=["video", "photo"],
            qualitative_preferences={"stated_priority": "video"}
        )
        
        top_ids = [c["candidate_id"] for c in res["top_recommendations"]]
        dominated_ids = [c["candidate_id"] for c in res["pareto_dominated_candidates"]]
        
        self.assertIn("CAM-A", top_ids)
        self.assertIn("CAM-B", top_ids)
        self.assertNotIn("CAM-C", top_ids)
        self.assertIn("CAM-C", dominated_ids)
        self.assertIn("CAM-A", res["pareto_dominated_candidates"][0]["dominated_by"])
        self.assertIn("CAM-B", res["pareto_dominated_candidates"][0]["dominated_by"])

    def test_03_inspectable_preference_weights(self):
        """Pass path: Weights are inspectable and transparently documented."""
        weight_res = derive_preference_weights(
            qualitative_preferences={"stated_priority": "video"},
            evaluated_dimensions=["video", "photo", "battery"]
        )
        self.assertTrue(weight_res["is_inspectable"])
        self.assertFalse(weight_res["silent_invented_decimals"])
        self.assertEqual(weight_res["weights"]["video"], 0.6)
        self.assertEqual(weight_res["weights"]["photo"], 0.2)
        self.assertEqual(weight_res["weights"]["battery"], 0.2)
        self.assertEqual(len(weight_res["derivation_explanations"]), 3)

    def test_04_adversarial_vague_input_no_silent_random_decimal(self):
        """Adversarial path: Vague preference '比较看重视频' cannot produce silent uninspected decimal weights."""
        weight_res = derive_preference_weights(
            qualitative_preferences={"stated_priority": "video"},
            evaluated_dimensions=["video", "audio"]
        )
        self.assertTrue(weight_res["is_inspectable"])
        # Derivation explanation must explicitly exist
        self.assertIn("Primary focus tier (0.6) assigned to 'video'", weight_res["derivation_explanations"][0])

if __name__ == "__main__":
    unittest.main()
