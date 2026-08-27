#!/usr/bin/env python3
"""Test suite for Ticket 07: Implement S/A/B/U evidence confidence and separate maturity labels.
Tests both happy path and adversarial conditions:
1. S/A/B/U evidence confidence calculation based on critical claim coverage.
2. Maturity pool assignment (mature_recommendations, conditional_recommendations, watch_list, excluded).
3. New products with strong short-term evidence receive conditional_recommendations with Grade A, not legacy 'B blackhorse'.
4. Adversarial path: High-volume mature product (36 months) with disputed critical claims cannot receive Grade S.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_confidence_engine import calculate_evidence_grade, assign_maturity_pool

class TestTicket07ConfidenceMaturity(unittest.TestCase):
    def test_01_evidence_grade_hierarchy(self):
        """Pass path: Evaluates S, A, B, and U evidence confidence correctly."""
        # 1. Authoritative verified -> S
        claims_s = [
            {"claim": "Official 3C", "impact": "critical", "status": "verified", "evidence_grade": "S", "source_role_appropriate": True},
            {"claim": "Lab efficiency 92%", "impact": "high", "status": "verified", "evidence_grade": "S", "source_role_appropriate": True}
        ]
        res_s = calculate_evidence_grade(claims_s)
        self.assertEqual(res_s["grade"], "S")
        
        # 2. Substantial verified -> A
        claims_a = [
            {"claim": "Official spec", "impact": "critical", "status": "verified", "evidence_grade": "A", "source_role_appropriate": True},
            {"claim": "Lab test 88%", "impact": "high", "status": "verified", "evidence_grade": "A", "source_role_appropriate": True}
        ]
        res_a = calculate_evidence_grade(claims_a)
        self.assertEqual(res_a["grade"], "A")
        
        # 3. Disputed -> B
        claims_b = [
            {"claim": "Power output", "impact": "critical", "status": "disputed", "evidence_grade": "B", "source_role_appropriate": True}
        ]
        res_b = calculate_evidence_grade(claims_b)
        self.assertEqual(res_b["grade"], "B")
        
        # 4. Unverified -> U
        claims_u = [
            {"claim": "Durability", "impact": "critical", "status": "unverified", "evidence_grade": "U", "source_role_appropriate": None}
        ]
        res_u = calculate_evidence_grade(claims_u)
        self.assertEqual(res_u["grade"], "U")

    def test_02_new_product_is_conditional_with_grade_a(self):
        """Pass path: A sparse new product with strong short-term lab data is conditional with grade A, not legacy 'B blackhorse'."""
        claims = [
            {"claim": "Lab measured performance", "impact": "critical", "status": "verified", "evidence_grade": "A", "source_role_appropriate": True}
        ]
        grade_res = calculate_evidence_grade(claims)
        self.assertEqual(grade_res["grade"], "A")
        
        product = {
            "name": "Brand New Flagship Monitor",
            "market_months": 1,
            "has_long_term_durability_data": False,
            "excluded": False
        }
        pool = assign_maturity_pool(product, evidence_grade=grade_res["grade"], hard_constraints_pass=True)
        self.assertEqual(pool, "conditional_recommendations")

    def test_03_adversarial_mature_product_with_disputed_claim_cannot_receive_grade_s(self):
        """Adversarial path: A mature, 3-year-old popular product with conflicting critical evidence must NOT receive Grade S merely because of age."""
        disputed_claims = [
            {"claim": "Coil whine defect level", "impact": "critical", "status": "disputed", "evidence_grade": "B", "source_role_appropriate": True},
            {"claim": "Rated continuous power", "impact": "high", "status": "verified", "evidence_grade": "S", "source_role_appropriate": True}
        ]
        
        grade_res = calculate_evidence_grade(disputed_claims)
        
        # Must be Grade B due to conflict, never S
        self.assertNotEqual(grade_res["grade"], "S")
        self.assertEqual(grade_res["grade"], "B")
        
        product_mature_popular = {
            "name": "Classic Bestseller PSU 2023",
            "market_months": 36,
            "has_long_term_durability_data": True,
            "critical_risk_disputed": True,
            "excluded": False
        }
        
        pool = assign_maturity_pool(product_mature_popular, evidence_grade=grade_res["grade"], hard_constraints_pass=True)
        self.assertIn(pool, ["conditional_recommendations", "watch_list"])
        self.assertNotEqual(pool, "mature_recommendations")

if __name__ == "__main__":
    unittest.main()
