#!/usr/bin/env python3
"""Test suite for Ticket 15: Make Round 1 adaptive and cap conversation at three rounds.
Tests:
1. Pass: Fully specified intake triggers direct delivery without unnecessary clarification rounds.
2. Pass: Broad search explores +40% headroom (2000 budget -> 2800 search ceiling) without premature truncation.
3. Pass: Already supplied variables are not re-asked.
4. Pass: Turn 3 strictly enforces final decision delivery (capped at 3 rounds max).
5. Adversarial: Minimal query '推荐个咖啡机' generates 2-3 engineering/use questions, forbidding presentation/channel questions.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adaptive_round1_engine import (
    conduct_broad_prior_exploration,
    evaluate_intake_and_generate_clarifications,
    FORBIDDEN_ROUND_1_TOPICS
)

class TestTicket15Round1(unittest.TestCase):
    def test_01_fully_specified_intake_direct_delivery(self):
        """Pass path: Fully specified case goes directly to final decision delivery."""
        res = evaluate_intake_and_generate_clarifications(
            category="espresso_machine",
            user_query="Need 58mm commercial portafilter espresso machine with dual PID, under 4000 CNY",
            supplied_variables={
                "usage_scenario": "2-3 shots daily",
                "physical_constraints": "Countertop depth < 40cm",
                "primary_priority": "thermal stability"
            },
            turn_number=1,
            declared_budget_cny=4000.0
        )
        self.assertTrue(res["direct_delivery"])
        self.assertEqual(len(res["questions"]), 0)

    def test_02_broad_exploration_headroom(self):
        """Pass path: Broad search on 2000 CNY budget explores up to 2800 CNY (+40%) for physics grounding."""
        exp = conduct_broad_prior_exploration(category="espresso_machine", declared_budget_cny=2000.0)
        self.assertEqual(exp["declared_budget"], 2000.0)
        self.assertEqual(exp["search_ceiling_cny"], 2800.0)
        self.assertFalse(exp["prematurely_truncated"])
        self.assertGreater(len(exp["physics_grounding_topics"]), 0)

    def test_03_no_reasking_supplied_variables(self):
        """Pass path: Already provided variables are not re-asked."""
        res = evaluate_intake_and_generate_clarifications(
            category="espresso_machine",
            user_query="Looking for an espresso machine, already have space dimensions 30x30cm",
            supplied_variables={"physical_constraints": "30x30cm"},
            turn_number=1
        )
        asked_vars = [q["variable"] for q in res["questions"]]
        self.assertNotIn("physical_constraints", asked_vars)
        self.assertIn("physical_constraints", res["already_supplied_not_reasked"])

    def test_04_hard_cap_at_three_rounds(self):
        """Pass path: Turn 3 forces direct delivery, capping clarification at 2 rounds max."""
        res = evaluate_intake_and_generate_clarifications(
            category="espresso_machine",
            user_query="still thinking",
            supplied_variables={},
            turn_number=3
        )
        self.assertTrue(res["direct_delivery"])
        self.assertEqual(len(res["questions"]), 0)
        self.assertIn("Hard conversation cap reached", res["reason"])

    def test_05_adversarial_minimal_query_asks_engineering_not_view_choices(self):
        """Adversarial path: Minimal query '推荐个咖啡机' asks 2-3 physical/use questions, NEVER presentation/market choices."""
        res = evaluate_intake_and_generate_clarifications(
            category="espresso_machine",
            user_query="推荐个咖啡机",
            supplied_variables={},
            turn_number=1
        )
        self.assertFalse(res["direct_delivery"])
        self.assertLessEqual(len(res["questions"]), 3)
        self.assertGreaterEqual(len(res["questions"]), 2)
        
        for q in res["questions"]:
            # Must strictly not be in forbidden presentation or market scope topics
            self.assertNotIn(q["topic"], FORBIDDEN_ROUND_1_TOPICS)
            self.assertIn(q["topic"], ["physical_dimensions_and_installation", "core_use_case", "tradeoff_priority"])

if __name__ == "__main__":
    unittest.main()
