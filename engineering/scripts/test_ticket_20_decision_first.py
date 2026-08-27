#!/usr/bin/env python3
"""Test suite for Ticket 20: Deliver concise decision-first output with dynamic candidates.
Tests:
1. Pass: 'just tell me what to buy' produces single decisive top choice without bloated matrix.
2. Pass: 3 viable candidates produce compact, non-empty 3-row comparison table.
3. Pass: Decision record is cleanly enclosed in <decision_record> XML tag.
4. Adversarial: Generating empty columns or bloated tables for trivial 60-yuan purchase fails validation.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decision_first_renderer import (
    render_decision_first_output,
    validate_output_conciseness,
    is_extreme_brevity_requested
)

class TestTicket20DecisionFirst(unittest.TestCase):
    def test_01_extreme_brevity_single_decisive_choice(self):
        """Pass path: 'just tell me which one' & 'direct recommendation' output single decisive top recommendation."""
        self.assertTrue(is_extreme_brevity_requested("just tell me which one"))
        self.assertTrue(is_extreme_brevity_requested("Give me a direct recommendation please"))
        self.assertTrue(is_extreme_brevity_requested("直接告诉我买哪个"))
        
        query = "just tell me which one"
        self.assertTrue(is_extreme_brevity_requested(query))
        cands = [
            {"name": "Charger GaN 65W", "price": 69, "core_reason": "Dual-port, compact foldable plug, low ripple under load."}
        ]
        
        rendered = render_decision_first_output(
            user_query=query,
            top_candidates=cands,
            decision_summary="Best value 65W charger for daily travel",
            within_budget_compromise="No 100W laptop high-draw support",
            research_budget="R0"
        )
        
        self.assertIn("首选推荐：Charger GaN 65W (¥69)", rendered)
        self.assertNotIn("|", rendered) # No comparison table in extreme brevity mode
        
        val = validate_output_conciseness(rendered, is_trivial_purchase=True, is_extreme_brevity=True)
        self.assertTrue(val["valid"])
        self.assertTrue(val["has_decision_first"])

    def test_02_three_candidates_compact_table(self):
        """Pass path: 3 viable candidates produce compact 3-row comparison."""
        cands = [
            {"name": "Camera A", "price": 5999, "tech_route": "24MP BSI", "advantage": "High AF speed", "tradeoff": "8-bit video"},
            {"name": "Camera B", "price": 6499, "tech_route": "33MP Standard", "advantage": "High resolution", "tradeoff": "Rolling shutter"},
            {"name": "Camera C", "price": 5499, "tech_route": "20MP Micro 4/3", "advantage": "Compact body", "tradeoff": "Low light noise"}
        ]
        rendered = render_decision_first_output(
            user_query="Need a hybrid camera under 7000",
            top_candidates=cands,
            decision_summary="Camera A balances autofocus reliability and low-light performance within budget.",
            within_budget_compromise="Compromised on 10-bit internal recording vs flagship tier",
            decision_record_payload={"case_id": "D-001", "decision": "Camera A"}
        )
        
        self.assertIn("## 首选决策：Camera A", rendered)
        self.assertIn("| Camera A | ¥5999 |", rendered)
        self.assertIn("| Camera B | ¥6499 |", rendered)
        self.assertIn("| Camera C | ¥5499 |", rendered)
        self.assertIn("<decision_record>", rendered)
        self.assertIn("</decision_record>", rendered)

        val = validate_output_conciseness(rendered, is_trivial_purchase=False, is_extreme_brevity=False)
        self.assertTrue(val["valid"])
        self.assertFalse(val["has_empty_cell"])

    def test_03_adversarial_bloated_trivial_purchase_fails_validation(self):
        """Adversarial path: Generating empty table padding or 30+ lines on trivial purchase fails."""
        bloated_text = "## 介绍\n" + "\n".join([f"Line {i} of methodology padding" for i in range(35)])
        val = validate_output_conciseness(bloated_text, is_trivial_purchase=True)
        self.assertFalse(val["valid"])

    def test_04_adversarial_extreme_brevity_with_table_fails_validation(self):
        """Adversarial path: Outputting a table when extreme brevity was requested fails."""
        text_with_table = "## 首选推荐：Charger X\n| Col A | Col B |\n|---|---|\n| 1 | 2 |"
        val = validate_output_conciseness(text_with_table, is_extreme_brevity=True)
        self.assertFalse(val["valid"])
        self.assertIn("Extreme brevity requested but comparison table was generated", val["reason"])

if __name__ == "__main__":
    unittest.main()
