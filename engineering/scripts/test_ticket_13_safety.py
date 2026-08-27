#!/usr/bin/env python3
"""Test suite for Ticket 13: Replace incident-count rules with scoped safety-signal adjudication.
Tests:
1. Pass: Official recall on current revision triggers hard exclusion.
2. Pass: Defect in Rev A isolates and does not exclude fixed Rev B (scoped exclusion).
3. Pass: 3 complaints on 5,000,000 units classified as watch point rather than common defect.
4. Pass: Cross-platform duplicate complaints from same user are deduplicated into single incident.
5. Adversarial: Unverified single forum fire anecdote triggers risk signal disclosure without instant product veto.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from safety_adjudication_engine import adjudicate_safety_signal

class TestTicket13Safety(unittest.TestCase):
    def test_01_official_recall_triggers_hard_exclude(self):
        """Pass path: Official SAMR/CPSC recall on current revision triggers hard exclusion."""
        res = adjudicate_safety_signal(
            signal_id="SIG-001",
            product_entity={"model": "Heater Pro", "revision": "Rev A"},
            source_type="official_recall",
            incident_description="Thermal fuse failure under sustained load",
            reported_incidents=[{"user_id": "SAMR_BULLETIN_2026_08"}],
            affected_revisions=["Rev A"],
            has_official_regulatory_action=True
        )
        self.assertEqual(res["decision_impact"], "hard_exclude")
        self.assertTrue(res["hard_exclude"])

    def test_02_revision_isolation_allows_clean_revision(self):
        """Pass path: Early batch/revision defect isolates and does not exclude updated Rev B."""
        res = adjudicate_safety_signal(
            signal_id="SIG-002",
            product_entity={"model": "Heater Pro", "revision": "Rev B"},
            source_type="official_recall",
            incident_description="Rev A thermal fuse failure",
            reported_incidents=[{"user_id": "SAMR_BULLETIN_2026_08"}],
            affected_revisions=["Rev A"],
            has_official_regulatory_action=True
        )
        self.assertEqual(res["decision_impact"], "scoped_exclude_batch")
        self.assertFalse(res["hard_exclude"])
        self.assertIn("cleared", res["rationale"])

    def test_03_denominator_exposure_prevents_false_common_defect(self):
        """Pass path: 3 complaints across 5,000,000 units are classified as watch point."""
        incidents = [
            {"user_id": "user_a", "desc": "Coil whine"},
            {"user_id": "user_b", "desc": "Coil whine"},
            {"user_id": "user_c", "desc": "Coil whine"}
        ]
        res = adjudicate_safety_signal(
            signal_id="SIG-003",
            product_entity={"model": "Popular Router X", "revision": "Rev A"},
            source_type="lab_test",
            incident_description="Minor inductor vibration",
            reported_incidents=incidents,
            exposure_volume=5000000
        )
        self.assertEqual(res["decision_impact"], "watch_point")
        self.assertFalse(res["hard_exclude"])

    def test_04_cross_platform_deduplication(self):
        """Pass path: Multiple forum posts by the same user across platforms are deduplicated."""
        incidents = [
            {"user_id": "tech_guy_99", "platform": "tieba", "desc": "Screen flickers"},
            {"user_id": "tech_guy_99", "platform": "xiaohongshu", "desc": "Screen flickers"}
        ]
        res = adjudicate_safety_signal(
            signal_id="SIG-004",
            product_entity={"model": "Monitor Y", "revision": "Rev A"},
            source_type="user_forum",
            incident_description="Screen flicker reported",
            reported_incidents=incidents
        )
        # Stage 3 deduplication count must be 1
        dedup_stage = [s for s in res["stages"] if s["stage"] == "3_deduplication"][0]
        self.assertEqual(dedup_stage["deduped_count"], 1)

    def test_05_adversarial_single_forum_anecdote_no_instant_veto(self):
        """Adversarial path: 1 unverified forum fire post cannot cause product-wide hard exclusion."""
        res = adjudicate_safety_signal(
            signal_id="SIG-005",
            product_entity={"model": "Phone Z", "revision": "Rev A"},
            source_type="user_forum",
            incident_description="Anonymous forum post claiming battery smoke",
            reported_incidents=[{"user_id": "anon_forum_user", "source_post_url": "http://forum.xyz/post/1"}]
        )
        
        # Must be classified as risk_signal_disclosure, strictly NOT hard_exclude
        self.assertNotEqual(res["decision_impact"], "hard_exclude")
        self.assertEqual(res["decision_impact"], "risk_signal_disclosure")
        self.assertFalse(res["hard_exclude"])

if __name__ == "__main__":
    unittest.main()
