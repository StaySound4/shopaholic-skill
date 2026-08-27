#!/usr/bin/env python3
"""Test suite for Ticket 16: Make Round 2 search-informed and optional.
Tests:
1. Pass: Camera search finds used flagship at same price and asks used acceptance (category-eligible).
2. Pass: Baby car seat query strictly skips used questions (category-ineligible).
3. Pass: Clear request / single survivor skips Round 2 entirely.
4. Adversarial: Asking user for matrix/layout format preferences is strictly rejected.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adaptive_round2_engine import (
    evaluate_round2_necessity,
    is_category_eligible_for_used,
    validate_question_safety
)

class TestTicket16Round2(unittest.TestCase):
    def test_01_camera_used_flagship_triggers_question(self):
        """Pass path: Inspectable camera category with discovered discontinued flagship asks used acceptance."""
        self.assertTrue(is_category_eligible_for_used("camera_body"))
        
        survivors = [
            {"model": "Mid-tier Camera New", "condition": "new", "price": 8000},
            {"model": "Flagship Pro Camera Used", "condition": "used", "is_discontinued_flagship": True, "price": 8000}
        ]
        
        res = evaluate_round2_necessity(
            category="camera_body",
            research_survivors=survivors,
            user_declared_preferences={}
        )
        self.assertFalse(res["skip_round_2"])
        self.assertEqual(len(res["questions"]), 1)
        self.assertEqual(res["questions"][0]["topic"], "used_vs_new_tradeoff")
        self.assertIn("prior-generation flagship", res["questions"][0]["question"])

    def test_02_baby_car_seat_skips_used_question(self):
        """Pass path: Baby car seat is strictly ineligible for used goods and must skip used questions."""
        self.assertFalse(is_category_eligible_for_used("baby_car_seat"))
        
        survivors = [
            {"model": "Car Seat A", "condition": "new", "price": 2000},
            {"model": "Car Seat B Used", "condition": "used", "price": 2000}
        ]
        
        res = evaluate_round2_necessity(
            category="baby_car_seat",
            research_survivors=survivors,
            user_declared_preferences={}
        )
        self.assertTrue(res["skip_round_2"])
        self.assertEqual(len(res["questions"]), 0)

    def test_03_single_survivor_skips_round_2(self):
        """Pass path: Single clear survivor skips Round 2 directly to delivery."""
        res = evaluate_round2_necessity(
            category="espresso_machine",
            research_survivors=[{"model": "Dual PID Espresso Machine", "condition": "new"}],
            user_declared_preferences={}
        )
        self.assertTrue(res["skip_round_2"])
        self.assertEqual(len(res["questions"]), 0)
        self.assertIn("Clear dominant candidate", res["reason"])

    def test_04_adversarial_format_and_matrix_questions_strictly_forbidden(self):
        """Adversarial path: Questions inquiring about presentation formats, matrix, or tables are rejected."""
        self.assertFalse(validate_question_safety("Do you prefer a dual-track matrix or card view?"))
        self.assertFalse(validate_question_safety("Should I output a Markdown table layout for you?"))
        self.assertFalse(validate_question_safety("Choose your presentation format preferences."))
        
        # Valid engineering question passes
        self.assertTrue(validate_question_safety("Do you prioritize dark-room contrast or peak daylight brightness?"))

if __name__ == "__main__":
    unittest.main()
