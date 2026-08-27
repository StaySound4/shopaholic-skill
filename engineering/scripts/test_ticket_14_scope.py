#!/usr/bin/env python3
"""Test suite for Ticket 14: Separate global evidence scope from purchase and output market scope.
Tests:
1. Pass: China-only purchase consults global registries (VESA, FCC) and recommends only CN-purchasable SKU.
2. Pass: Exposes uncertified marketing claim (claimed HDR1000 disputed against official VESA registry).
3. Pass: Exposes component downgrades using global teardown / FCC records.
4. Adversarial: Global evidence lookup must NEVER silently mutate purchase_scope to 'both'.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scope_separator_engine import ScopeContext, cross_verify_with_global_evidence

class TestTicket14Scope(unittest.TestCase):
    def test_01_china_purchase_excludes_overseas_candidate(self):
        """Pass path: China-only purchase consults global evidence but filters out overseas-only SKUs."""
        ctx = ScopeContext(purchase_scope="cn", output_scope="cn", evidence_scope="global")
        
        candidates = [
            {"model": "Monitor CN Edition", "market_availability": ["cn"]},
            {"model": "Monitor Global US Only", "market_availability": ["overseas"]},
            {"model": "Monitor Dual Market", "market_availability": ["cn", "overseas"]}
        ]
        
        filtered = ctx.filter_candidates(candidates)
        models = [c["model"] for c in filtered]
        
        self.assertIn("Monitor CN Edition", models)
        self.assertIn("Monitor Dual Market", models)
        self.assertNotIn("Monitor Global US Only", models)
        self.assertEqual(len(filtered), 2)

    def test_02_global_registry_exposes_fake_hdr_claim(self):
        """Pass path: Domestic marketing claims HDR1000, but official VESA registry only certifies HDR600."""
        ctx = ScopeContext(purchase_scope="cn", output_scope="cn", evidence_scope="global")
        domestic_claim = {"claim_name": "HDR_Tier", "claimed_value": "DisplayHDR 1000"}
        global_registry = {"certified": True, "certified_tier": "DisplayHDR 600"}
        
        res = cross_verify_with_global_evidence(
            domestic_claim=domestic_claim,
            global_registry_evidence=global_registry,
            scope_context=ctx
        )
        
        self.assertEqual(res["status"], "disputed")
        self.assertTrue(res["cmd_discrepancy_detected"])
        self.assertIn("lower tier", res["notes"])

    def test_03_fcc_teardown_exposes_component_downgrade(self):
        """Pass path: Global teardown / FCC filing reveals domestic heatsink downgrade."""
        ctx = ScopeContext(purchase_scope="cn", output_scope="cn", evidence_scope="global")
        domestic_claim = {"claim_name": "Cooling_Solution", "claimed_value": "8-Heatpipe Chamber"}
        fcc_evidence = {
            "global_sku_spec": "8 copper heatpipes + vapor chamber",
            "domestic_sku_spec": "4 copper heatpipes (downgraded)"
        }
        
        res = cross_verify_with_global_evidence(
            domestic_claim=domestic_claim,
            fcc_or_teardown_evidence=fcc_evidence,
            scope_context=ctx
        )
        
        self.assertEqual(res["status"], "disputed")
        self.assertTrue(res["cmd_discrepancy_detected"])
        self.assertIn("downgrade detected", res["notes"])

    def test_04_adversarial_global_evidence_cannot_mutate_purchase_scope(self):
        """Adversarial path: Querying global evidence must not silently mutate purchase_scope to 'both'."""
        ctx = ScopeContext(purchase_scope="cn", output_scope="cn", evidence_scope="global")
        
        # Verify domestic claim against international FCC records
        res = cross_verify_with_global_evidence(
            domestic_claim={"claim_name": "RF_Power", "claimed_value": "20dBm"},
            global_registry_evidence={"certified": True, "certified_tier": "20dBm"},
            scope_context=ctx
        )
        
        # Scope context and result must maintain purchase_scope == 'cn'
        self.assertEqual(ctx.purchase_scope, "cn")
        self.assertEqual(res["purchase_scope"], "cn")
        self.assertNotEqual(ctx.purchase_scope, "both")

if __name__ == "__main__":
    unittest.main()
