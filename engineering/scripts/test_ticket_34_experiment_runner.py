#!/usr/bin/env python3
"""Test suite for Ticket 34: Run the first real paired baseline/full/ablation experiment.
Tests:
1. Pass: Experiment manifest is schema-compliant, hash-locked across all 11 conditions, and runs are accounted.
2. Pass: Run records strictly adhere to run-record.schema.json.
3. Pass: Blocked/failed runs are accounted for separately.
4. Adversarial: Post-lock mutation of test cases immediately invalidates the manifest signature.
"""
import unittest, sys, copy, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from experiment_runner_engine import (
    PREREGISTERED_CONDITIONS,
    create_experiment_manifest,
    verify_manifest_integrity,
    create_run_record,
    account_experiment_run_statuses
)

class TestTicket34ExperimentRunner(unittest.TestCase):
    def setUp(self):
        self.sample_cases = [
            {"case_id": "EXP-01", "prompt": "Recommend a high-refresh OLED monitor under 4000"},
            {"case_id": "EXP-02", "prompt": "Recommend a baby stroller meeting GB 14748-2006"}
        ]

    def test_01_manifest_schema_and_hash_locking(self):
        """Pass path: Manifest contains all required fields from experiment-manifest.schema.json and 11 conditions."""
        manifest = create_experiment_manifest("EXP_RUN_2026_01", self.sample_cases)
        
        # Verify required properties
        required_props = [
            "experiment_id", "protocol_version", "created_at", "case_set_hash",
            "conditions", "replicates", "random_seed", "release_gates"
        ]
        for prop in required_props:
            self.assertIn(prop, manifest)

        self.assertEqual(len(manifest["conditions"]), 11)
        self.assertEqual(manifest["conditions"], PREREGISTERED_CONDITIONS)
        self.assertTrue(manifest["preregistered"])

        # Check integrity with unchanged cases
        valid, err = verify_manifest_integrity(manifest, self.sample_cases)
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_02_run_records_and_status_accounting(self):
        """Pass path: Run records adhere to schema and status accounting segregates complete, blocked, and failed runs."""
        run_records = []
        # Simulate standard runs
        for case in self.sample_cases:
            for cond in PREREGISTERED_CONDITIONS:
                rec = create_run_record(case["case_id"], cond, replicate=1, status="complete")
                run_records.append(rec)

        # Add 1 blocked run and 1 fail run
        run_records.append(create_run_record("EXP-03", "T_full", replicate=1, status="BLOCKED_SOURCE"))
        run_records.append(create_run_record("EXP-04", "T_full", replicate=1, status="FAIL_PRODUCT"))

        # Verify run record required fields
        required_run_fields = [
            "run_id", "case_id", "condition", "replicate", "started_at", "status", "raw_output_path"
        ]
        for r in run_records:
            for field in required_run_fields:
                self.assertIn(field, r)

        # Account statuses
        accounting = account_experiment_run_statuses(run_records)
        self.assertEqual(accounting["total_runs"], len(self.sample_cases) * 11 + 2)
        self.assertEqual(accounting["complete_count"], len(self.sample_cases) * 11)
        self.assertEqual(accounting["blocked_source_count"], 1)
        self.assertEqual(accounting["fail_product_count"], 1)
        self.assertTrue(accounting["is_all_accounted"])

    def test_03_adversarial_post_lock_case_mutation_fails(self):
        """Adversarial path: Mutating a test case after manifest registration invalidates manifest."""
        manifest = create_experiment_manifest("EXP_RUN_2026_02", self.sample_cases)
        
        # Tamper with case list
        tampered_cases = copy.deepcopy(self.sample_cases)
        tampered_cases[0]["prompt"] = "MODIFIED PROMPT TO FAVOR TARGET SYSTEM"

        valid, err = verify_manifest_integrity(manifest, tampered_cases)
        self.assertFalse(valid)
        self.assertIn("Manifest hash mismatch", err)

if __name__ == "__main__":
    unittest.main()
