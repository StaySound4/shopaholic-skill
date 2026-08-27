#!/usr/bin/env python3
"""Test suite for Ticket 12: Use dynamic candidate count and marginal-information stop rule.
Tests:
1. Pass path: Discovery stops after 2 consecutive passes with zero marginal information gain and outputs justified count (e.g., exactly 3).
2. Dynamic count: Accurately outputs 0, 1, or 3 justified candidates without artificial quota padding.
3. Adversarial path: Repeated synonym queries that yield no new routes/findings cannot artificially prolong search or pad candidates.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from marginal_stop_engine import DiscoverySession

class TestTicket12StopRule(unittest.TestCase):
    def test_01_two_no_gain_passes_stops_discovery(self):
        """Pass path: Discovery stops when 2 consecutive passes produce no decision-relevant gain."""
        session = DiscoverySession(category="wireless_earbuds", research_budget="R1")
        
        # Pass 1: Discovers 2 candidates and new technology route (ANC hybrid)
        p1 = session.record_pass(
            query="hybrid ANC wireless earbuds",
            information_gains=[{"gain_type": "new_technology_route", "detail": "Hybrid dual-mic ANC architecture"}],
            unresolved_critical_claims=1,
            new_candidates=[{"model": "Buds Pro 1"}, {"model": "Buds Pro 2"}]
        )
        self.assertFalse(p1["stopped"])
        self.assertEqual(session.consecutive_no_gain_passes, 0)
        
        # Pass 2: Discovers Pareto candidate
        p2 = session.record_pass(
            query="LDAC supported low latency wireless earbuds",
            information_gains=[{"gain_type": "pareto_frontier_candidate", "detail": "Found low-latency + LDAC non-dominated option"}],
            unresolved_critical_claims=0,
            new_candidates=[{"model": "Buds Elite 3"}]
        )
        self.assertFalse(p2["stopped"])
        self.assertEqual(session.consecutive_no_gain_passes, 0)
        
        # Pass 3: Search yields no new technology route or pareto gain
        p3 = session.record_pass(
            query="best sounding bluetooth earphones 2026",
            information_gains=[],
            unresolved_critical_claims=0
        )
        self.assertFalse(p3["stopped"])
        self.assertEqual(session.consecutive_no_gain_passes, 1)
        
        # Pass 4: Second no-gain pass -> Must trigger stop rule
        p4 = session.record_pass(
            query="top wireless headphones under 1000",
            information_gains=[],
            unresolved_critical_claims=0
        )
        self.assertTrue(p4["stopped"])
        self.assertIn("Marginal information gain exhausted", p4["stop_reason"])
        
        # Finalize candidates -> Outputs exactly 3 justified items with no padding
        final = session.finalize_candidates(session.discovered_candidates)
        self.assertEqual(final["candidate_count"], 3)
        self.assertFalse(final["padding_applied"])

    def test_02_zero_or_single_candidate_without_padding(self):
        """Pass path: Final can contain 0 or 1 candidates when strict constraints exclude alternatives without padding."""
        session = DiscoverySession(category="specialized_monitor", research_budget="R2")
        
        # Only 1 candidate satisfies hard physical constraints
        final = session.finalize_candidates([{"model": "Medical Monitor Alpha"}])
        self.assertEqual(final["candidate_count"], 1)
        self.assertFalse(final["padding_applied"])
        
        # Zero candidates when all fail hard safety constraints
        final_zero = session.finalize_candidates([])
        self.assertEqual(final_zero["candidate_count"], 0)
        self.assertFalse(final_zero["padding_applied"])

    def test_03_adversarial_synonym_repeats_cannot_prolong_search(self):
        """Adversarial path: Repeating synonym searches with zero new information gain cannot bypass stop rule to fulfill quota."""
        session = DiscoverySession(category="phone_charger", research_budget="R0")
        
        # Pass 1: Discovers 2 standard GaN chargers
        session.record_pass(
            query="65W GaN fast charger",
            information_gains=[{"gain_type": "value_frontier_entry", "detail": "65W dual port GaN"}],
            unresolved_critical_claims=0,
            new_candidates=[{"model": "GaN 65W A"}, {"model": "GaN 65W B"}]
        )
        
        # Pass 2: Synonym search with no new info gain
        session.record_pass(
            query="65 watt gallium nitride quick charging head",
            information_gains=[],
            unresolved_critical_claims=0
        )
        
        # Pass 3: Another synonym search with no new info gain -> MUST STOP immediately on 2nd consecutive pass
        p3 = session.record_pass(
            query="super fast 65w phone plug brick",
            information_gains=[],
            unresolved_critical_claims=0
        )
        
        self.assertTrue(p3["stopped"])
        self.assertEqual(session.consecutive_no_gain_passes, 2)

if __name__ == "__main__":
    unittest.main()
