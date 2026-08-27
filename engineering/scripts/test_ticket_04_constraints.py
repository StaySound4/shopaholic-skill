#!/usr/bin/env python3
"""Test suite for Ticket 04: Replace H/S with three constraint classes.
Tests both happy path and adversarial conditions:
1. Strict exclusion of candidates violating safety_compatibility_hard or user_declared_hard.
2. User declared hard: budget <= 3000 strictly excludes 3299 CNY candidate.
3. User declared hard: required HomeKit ecosystem strictly excludes non-HomeKit candidate.
4. Search vs Delivery decoupling: 4500 CNY flagship is captured for physics grounding but strictly excluded from final recommendations.
5. Soft preference ranking: Soft preferences rank candidates but do not masquerade as safety/physical impossibility.
6. Adversarial path: Color preference alone must NOT be classified as safety_compatibility_hard.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from constraint_engine import classify_constraint, evaluate_candidate_constraints, process_candidate_pools

class TestTicket04Constraints(unittest.TestCase):
    def test_01_constraint_classification(self):
        """Pass path: Constraints are accurately mapped to the three canonical classes."""
        self.assertEqual(classify_constraint("220V voltage compatibility"), "safety_compatibility_hard")
        self.assertEqual(classify_constraint("Must be free from active recall"), "safety_compatibility_hard")
        self.assertEqual(classify_constraint("Budget under 3000 CNY"), "user_declared_hard")
        self.assertEqual(classify_constraint("Exclude brand Dyson"), "user_declared_hard")
        self.assertEqual(classify_constraint("Must support Apple HomeKit"), "user_declared_hard")
        self.assertEqual(classify_constraint("Prefer matte black color"), "soft_preference")
        self.assertEqual(classify_constraint("Prefer lighter weight under 500g"), "soft_preference")

    def test_02_strict_exclusion_on_budget_and_ecosystem(self):
        """Pass path: budget <= 3000 strictly excludes 3299 CNY; HomeKit requirement strictly excludes non-HomeKit."""
        constraints = {
            "safety_compatibility_hard": [],
            "user_declared_hard": [
                {"key": "max_budget", "value": 3000},
                {"key": "required_ecosystem", "ecosystem": "HomeKit"}
            ],
            "soft_preference": [{"key": "color", "value": "black"}]
        }
        
        candidates = [
            {"name": "Device A (Valid)", "price": 2800, "supported_ecosystems": ["HomeKit", "Alexa"], "color": "black"},
            {"name": "Device B (Over-budget)", "price": 3299, "supported_ecosystems": ["HomeKit"], "color": "black"},
            {"name": "Device C (No HomeKit)", "price": 2500, "supported_ecosystems": ["Tuya"], "color": "black"}
        ]
        
        res = process_candidate_pools(candidates, constraints)
        surviving = res["surviving_recommendations"]
        excluded = res["excluded_candidates"]
        
        # Surviving must ONLY contain Device A
        self.assertEqual(len(surviving), 1)
        self.assertEqual(surviving[0]["name"], "Device A (Valid)")
        
        # Excluded must contain Device B and Device C with exact violation classes
        self.assertEqual(len(excluded), 2)
        ex_names = [e["candidate"]["name"] for e in excluded]
        self.assertIn("Device B (Over-budget)", ex_names)
        self.assertIn("Device C (No HomeKit)", ex_names)
        
        # Check reasons
        b_violation = next(e["evaluation"]["violations"][0] for e in excluded if e["candidate"]["name"] == "Device B (Over-budget)")
        self.assertEqual(b_violation["constraint_class"], "user_declared_hard")
        self.assertIn("exceeds declared user budget cap", b_violation["reason"])

    def test_03_search_delivery_decoupling_with_physics_grounding(self):
        """Pass path: Broad search ingests 4500 CNY flagship physics to explain 3000 CNY compromises without recommending it."""
        constraints = {
            "safety_compatibility_hard": [],
            "user_declared_hard": [{"key": "max_budget", "value": 3000}],
            "soft_preference": []
        }
        
        candidates = [
            {"name": "Budget Pick 1", "price": 2700, "physics_insights": "Uses 2-layer membrane"},
            {"name": "Flagship Benchmark (4500)", "price": 4200, "physics_insights": "Uses 3-layer Gore-Tex Pro 28000mm"}
        ]
        
        res = process_candidate_pools(candidates, constraints, search_headroom_multiplier=1.5)
        
        # Recommendations must strictly exclude the 4200 flagship
        self.assertEqual(len(res["surviving_recommendations"]), 1)
        self.assertEqual(res["surviving_recommendations"][0]["name"], "Budget Pick 1")
        
        # Flagship benchmark must be isolated in grounding pool
        self.assertEqual(len(res["flagship_benchmarks_for_grounding"]), 1)
        self.assertEqual(res["flagship_benchmarks_for_grounding"][0]["candidate"], "Flagship Benchmark (4500)")
        self.assertEqual(res["flagship_benchmarks_for_grounding"][0]["role"], "search_headroom_physics_benchmark")

    def test_04_adversarial_soft_preference_cannot_masquerade_as_safety(self):
        """Adversarial path: Color preference alone must NOT be treated as a safety/physical exclusion."""
        classified_class = classify_constraint("I would love a white colored model if available")
        self.assertNotEqual(classified_class, "safety_compatibility_hard")
        self.assertEqual(classified_class, "soft_preference")
        
        # Evaluate candidate with mismatched color
        candidate = {"name": "Product Silver", "color": "silver", "price": 1000}
        safety_hard = []
        user_hard = []
        soft_prefs = [{"key": "color", "value": "white"}]
        
        eval_res = evaluate_candidate_constraints(candidate, safety_hard, user_hard, soft_prefs)
        
        # Must NOT be excluded
        self.assertTrue(eval_res["eligible_for_recommendation"])
        self.assertFalse(eval_res["excluded"])
        self.assertEqual(len(eval_res["violations"]), 0)
        self.assertEqual(eval_res["soft_preference_score"], 0.0)

if __name__ == "__main__":
    unittest.main()
