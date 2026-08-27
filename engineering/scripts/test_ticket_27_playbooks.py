#!/usr/bin/env python3
"""Test suite for Ticket 27: Modularize category knowledge as live-verification playbooks.
Tests:
1. Pass: Coffee query loads only coffee.md (strict single-category context isolation).
2. Pass: Coffee playbook tests ingredients/thermal compliance rather than universal BOM teardown.
3. Pass: HiFi query loads hifi-audio.md and prioritizes AP555/SINAD instrumented evidence over star reviews.
4. Pass: Tier 3 deep forensics loads conditionally for R2/R3 budgets.
5. Adversarial: Playbook relies on live wayfinding search anchors rather than static text hoarding.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from category_playbook_loader import load_progressive_category_context

class TestTicket27Playbooks(unittest.TestCase):
    def test_01_strict_single_category_context_isolation(self):
        """Pass path: Coffee query loads only coffee.md and isolates from other categories."""
        res = load_progressive_category_context("espresso_machine", research_budget="R1")
        self.assertTrue(res["tier_1_loaded"])
        self.assertEqual(res["tier_2_playbook"], "coffee.md")
        self.assertEqual(len(res["loaded_files"]), 1)
        self.assertIn("references/categories/coffee.md", res["loaded_files"])
        self.assertTrue(res["context_isolation_verified"])
        
        # Verify content contains coffee-specific physics
        content = res["playbook_content"]
        self.assertIn("Thermodynamic Stability", content)
        self.assertIn("GB 4806", content)
        self.assertNotIn("Audio Precision", content)
        self.assertNotIn("VESA DisplayHDR", content)

    def test_02_hifi_playbook_instrumented_testing(self):
        """Pass path: HiFi query loads hifi-audio.md prioritizing SINAD / THD+N over review stars."""
        res = load_progressive_category_context("hifi_headphone_amp", research_budget="R1")
        self.assertEqual(res["tier_2_playbook"], "hifi-audio.md")
        self.assertEqual(len(res["loaded_files"]), 1)
        
        content = res["playbook_content"]
        self.assertIn("SINAD", content)
        self.assertIn("THD+N", content)
        self.assertIn("Reject Subjective Review Stars", content)

    def test_03_tier_3_deep_forensics_activated_for_r3(self):
        """Pass path: R3 budget activates Tier 3 deep forensics."""
        res_r1 = load_progressive_category_context("baby_car_seat", research_budget="R1")
        res_r3 = load_progressive_category_context("baby_car_seat", research_budget="R3")
        
        self.assertFalse(res_r1["tier_3_deep_forensics"])
        self.assertTrue(res_r3["tier_3_deep_forensics"])
        self.assertEqual(res_r3["tier_2_playbook"], "infant-gear.md")

    def test_04_adversarial_live_wayfinding_anchors_avoid_static_hoarding(self):
        """Adversarial path: Playbooks embed live search anchors rather than static text hoarding."""
        res = load_progressive_category_context("gaming_monitor", research_budget="R1")
        self.assertEqual(res["tier_2_playbook"], "display-monitors.md")
        
        content = res["playbook_content"]
        self.assertIn("site:displayhdr.org/certified-products", content)
        self.assertIn("site:energylabel.gov.cn", content)
        self.assertIn("site:certipedia.com", content)

if __name__ == "__main__":
    unittest.main()
