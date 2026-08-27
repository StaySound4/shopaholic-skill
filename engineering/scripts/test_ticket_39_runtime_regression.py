#!/usr/bin/env python3
"""Test suite for Ticket 39: Run cross-runtime/model regression for every compatibility claim.
Tests:
1. Pass: Full matrix runs across 4 claimed configurations with critical cases.
2. Pass: Prompt-only runtime yields DEGRADED_PROMPT_ONLY, not hidden failure.
3. Adversarial: Removing a required tool produces BLOCKED_CAPABILITY, not FAIL_PRODUCT.
4. Adversarial: Untested runtime yields UNTESTED_CONFIGURATION, never generalized.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runtime_regression_engine import (
    execute_cross_runtime_case,
    run_regression_matrix_suite
)

class TestTicket39RuntimeRegression(unittest.TestCase):
    def setUp(self):
        self.critical_cases = [
            {"case_id": "REG-01", "required_tools": ["web_search", "read"], "prompt": "Verify GB 4706.1-2024 active status"},
            {"case_id": "REG-02", "required_tools": ["bash", "grep"], "prompt": "Check IEEE 1789 standard citation"}
        ]

    def test_01_full_matrix_regression(self):
        """Pass path: 4 configurations x 2 cases = 8 matrix runs with explicit results."""
        report = run_regression_matrix_suite(self.critical_cases)
        self.assertEqual(report["configurations_tested"], 4)
        self.assertEqual(report["total_matrix_runs"], 8)
        # chatgpt_web lacks all tools -> DEGRADED_PROMPT_ONLY for both cases
        degraded = [r for r in report["results"] if r["status"] == "DEGRADED_PROMPT_ONLY"]
        self.assertEqual(len(degraded), 2)
        # pi lacks grep -> REG-02 produces BLOCKED_CAPABILITY (1 case)
        blocked = [r for r in report["results"] if r["status"] == "BLOCKED_CAPABILITY"]
        self.assertEqual(len(blocked), 1)
        # Remaining 5 complete normally
        complete = [r for r in report["results"] if r["status"] == "complete"]
        self.assertEqual(len(complete), 5)

    def test_02_prompt_only_degraded_not_hidden(self):
        """Pass path: chatgpt_web runtime yields DEGRADED_PROMPT_ONLY, not FAIL_PRODUCT."""
        case = {"case_id": "REG-03", "required_tools": ["web_search"]}
        res = execute_cross_runtime_case(case, "chatgpt_web", "gpt-4o")
        self.assertEqual(res["status"], "DEGRADED_PROMPT_ONLY")
        self.assertIn("web_search", res["missing_tools"])
        self.assertNotEqual(res["status"], "FAIL_PRODUCT")

    def test_03_adversarial_missing_tool_produces_blocked_capability(self):
        """Adversarial path: Removing web_search from claude_code produces BLOCKED_CAPABILITY."""
        case = {"case_id": "REG-04", "required_tools": ["web_search", "read"]}
        res = execute_cross_runtime_case(
            case, "claude_code", "claude-3-7-sonnet",
            available_tools_override={"bash", "read", "grep"}  # web_search removed
        )
        self.assertEqual(res["status"], "BLOCKED_CAPABILITY")
        self.assertIn("web_search", res["missing_tools"])
        self.assertNotEqual(res["status"], "FAIL_PRODUCT")

    def test_04_adversarial_untested_runtime_not_generalized(self):
        """Adversarial path: Untested runtime yields UNTESTED_CONFIGURATION, never assumed compatible."""
        case = {"case_id": "REG-05", "required_tools": []}
        res = execute_cross_runtime_case(case, "cursor_ai", "gpt-4o")
        self.assertEqual(res["status"], "UNTESTED_CONFIGURATION")
        self.assertFalse(res["is_compatible"])

if __name__ == "__main__":
    unittest.main()
