#!/usr/bin/env python3
"""Test suite for Ticket 30: Add explicit degraded modes for source/tool unavailability.
Tests:
1. Pass: Inaccessible mandatory regulatory database produces BLOCKED_SOURCE degraded status.
2. Pass: Partial evidence produces bounded recommendation with degraded grade B/U and status partial.
3. Adversarial: Blog fallback attempting to replace regulator while retaining S grade is rejected.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from degraded_mode_engine import (
    handle_source_tool_unavailability,
    validate_degraded_grade_safety
)

class TestTicket30DegradedModes(unittest.TestCase):
    def test_01_mandatory_source_inaccessible_triggers_blocked(self):
        """Pass path: Inaccessible 3C database blocks verification and forbids hallucination."""
        res = handle_source_tool_unavailability(
            required_source_id="CN_3C_CNCA",
            is_source_accessible=False,
            fallback_sources=[],
            is_safety_critical=True
        )
        self.assertEqual(res["decision_status"], "blocked")
        self.assertEqual(res["eval_status"], "BLOCKED_SOURCE")
        self.assertEqual(res["evidence_grade"], "U")
        self.assertTrue(res["is_degraded"])
        self.assertTrue(res["retry_eligible"])
        self.assertIn("CN_3C_CNCA", res["blocked_source"])
        self.assertIn("prohibited", res["notes"])

    def test_02_partial_evidence_degrades_confidence(self):
        """Pass path: Offline primary database with secondary lab fallback produces partial status and grade B."""
        fallbacks = [
            {"source_id": "INDEPENDENT_LAB_TEARDOWN", "source_role": "independent_measurement"}
        ]
        res = handle_source_tool_unavailability(
            required_source_id="EU_EPREL",
            is_source_accessible=False,
            fallback_sources=fallbacks
        )
        self.assertEqual(res["decision_status"], "partial")
        self.assertEqual(res["eval_status"], "PARTIAL_EVIDENCE")
        self.assertEqual(res["evidence_grade"], "B")
        self.assertTrue(res["is_degraded"])

    def test_03_adversarial_blog_cannot_retain_s_grade_for_regulatory(self):
        """Adversarial path: Blog replacing regulatory source cannot retain S or A grade."""
        # Regulatory claim -> blog fallback -> S grade = ILLEGAL
        is_safe_s = validate_degraded_grade_safety(
            claim_type="3C_safety_certification",
            original_source_role="regulatory",
            actual_source_role="user_forum",
            assigned_grade="S"
        )
        self.assertFalse(is_safe_s)

        # Regulatory claim -> blog fallback -> U grade = SAFE
        is_safe_u = validate_degraded_grade_safety(
            claim_type="3C_safety_certification",
            original_source_role="regulatory",
            actual_source_role="user_forum",
            assigned_grade="U"
        )
        self.assertTrue(is_safe_u)

if __name__ == "__main__":
    unittest.main()
