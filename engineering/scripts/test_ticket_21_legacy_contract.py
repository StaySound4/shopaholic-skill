#!/usr/bin/env python3
"""Test suite for Ticket 21: Contract legacy L1-L4 and mature-A/blackhorse-B behavior.
Tests:
1. Pass: Migrates legacy tier_a_mature and tier_b_observation to 4 explicit canonical pools.
2. Pass: Canonical record with explicit pools passes legacy audit with zero violations.
3. Adversarial: Auditor catches and rejects forbidden legacy fields (tier_a_mature, l1_l4_truth_ranking).
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from legacy_contract_migrator import (
    migrate_legacy_candidate_pools,
    audit_record_for_legacy_leakage,
    VALID_EXPLICIT_POOLS
)

class TestTicket21LegacyContract(unittest.TestCase):
    def test_01_migrate_legacy_candidate_pools(self):
        """Pass path: Migrates legacy tier_a_mature / tier_b_observation to 4 explicit pools."""
        legacy_input = {
            "tier_a_mature": [
                {"name": "Mature Option 1", "condition": "new"},
                {"name": "Mature Option 2", "condition": "new"}
            ],
            "tier_b_observation": [
                {"name": "New Tech Watch Item", "condition": "new"},
                {"name": "Discontinued Flagship Option", "condition": "used", "is_conditional": True}
            ]
        }
        
        migrated = migrate_legacy_candidate_pools(legacy_input)
        
        # Verify all keys belong to the 4 explicit pools
        self.assertEqual(set(migrated.keys()), VALID_EXPLICIT_POOLS)
        self.assertEqual(len(migrated["mature_recommendations"]), 2)
        self.assertEqual(len(migrated["watch_list"]), 1)
        self.assertEqual(len(migrated["conditional_recommendations"]), 1)
        self.assertEqual(migrated["conditional_recommendations"][0]["name"], "Discontinued Flagship Option")
    def test_01b_merge_mixed_legacy_and_canonical_pools(self):
        """Pass path: Merges mixed legacy and existing canonical pools without dropping or overwriting."""
        mixed_input = {
            "tier_a_mature": [{"name": "Mature Legacy", "condition": "new"}],
            "tier_b_observation": [{"name": "Obs Legacy", "condition": "new"}],
            "mature_recommendations": [{"name": "Canonical Mature", "condition": "new"}],
            "watch_list": [{"name": "Canonical Watch", "condition": "new"}]
        }
        migrated = migrate_legacy_candidate_pools(mixed_input)
        mature_names = [c["name"] for c in migrated["mature_recommendations"]]
        watch_names = [c["name"] for c in migrated["watch_list"]]
        self.assertIn("Mature Legacy", mature_names)
        self.assertIn("Canonical Mature", mature_names)
        self.assertIn("Obs Legacy", watch_names)
        self.assertIn("Canonical Watch", watch_names)
        self.assertEqual(len(migrated["mature_recommendations"]), 2)
        self.assertEqual(len(migrated["watch_list"]), 2)

    def test_02_audit_clean_canonical_record(self):
        """Pass path: Canonical record passes audit with is_clean=True."""
        clean_record = {
            "case_id": "D-001",
            "candidate_pools": {
                "mature_recommendations": [{"name": "Cand A"}],
                "conditional_recommendations": [],
                "watch_list": [{"name": "Cand B"}],
                "excluded": []
            }
        }
        res = audit_record_for_legacy_leakage(clean_record)
        self.assertTrue(res["is_clean"])
        self.assertEqual(res["violation_count"], 0)

    def test_03_adversarial_legacy_fields_detected_and_rejected(self):
        """Adversarial path: Records containing tier_a_mature or l1_l4 fields are flagged."""
        dirty_record = {
            "case_id": "D-002",
            "l1_l4_truth_ranking": "L1",
            "candidate_pools": {
                "tier_a_mature": [{"name": "Old Cand"}],
                "invalid_pool_key": []
            }
        }
        res = audit_record_for_legacy_leakage(dirty_record)
        self.assertFalse(res["is_clean"])
        self.assertGreaterEqual(res["violation_count"], 2)
        
        violations_str = " ".join(res["violations"])
        self.assertIn("tier_a_mature", violations_str)
        self.assertIn("l1_l4", violations_str)

if __name__ == "__main__":
    unittest.main()
