#!/usr/bin/env python3
"""Test suite for Ticket 34: Run the first real paired baseline/full/ablation experiment.
Tests:
1. Pass: Experiment manifest is hash-locked across all 11 conditions, paired raw logs generated, and anti-cheat controls pass.
2. Adversarial: Post-lock mutation of test cases immediately invalidates the manifest signature.
"""
import unittest, sys, copy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from experiment_runner_engine import (
    ALL_CONDITIONS,
    create_experiment_manifest,
    verify_manifest_integrity,
    simulate_raw_run_execution,
    evaluate_anti_cheat_controls
)

class TestTicket34ExperimentRunner(unittest.TestCase):
    def setUp(self):
        self.sample_cases = [
            {"case_id": "EXP-01", "prompt": "Recommend a high-refresh OLED monitor under 4000"},
            {"case_id": "EXP-02", "prompt": "Recommend a baby stroller meeting GB 14748-2006"}
        ]

    def test_01_manifest_hash_locking_and_paired_execution(self):
        """Pass path: Manifest is hash-locked, 11 conditions run, anti-cheat controls pass."""
        manifest = create_experiment_manifest("EXP_RUN_2026_01", self.sample_cases)
        
        self.assertTrue(manifest["is_locked"])
        self.assertIn("manifest_signature", manifest)
        self.assertEqual(len(manifest["conditions"]), 11)
        self.assertIn("T_full", manifest["conditions"])
        self.assertIn("B1_uploaded_current", manifest["conditions"])
        self.assertIn("C_positive_bad_evidence", manifest["conditions"])
        self.assertIn("C_sham_style", manifest["conditions"])

        # Check integrity with unchanged cases
        valid, err = verify_manifest_integrity(manifest, self.sample_cases)
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Execute paired runs
        run_records = []
        for case in self.sample_cases:
            for cond in manifest["conditions"]:
                rec = simulate_raw_run_execution(case, cond, replicate=1)
                run_records.append(rec)

        self.assertEqual(len(run_records), len(self.sample_cases) * 11)

        # Evaluate anti-cheat controls
        anti_cheat = evaluate_anti_cheat_controls(run_records)
        self.assertTrue(anti_cheat["is_evaluator_valid"])
        self.assertTrue(anti_cheat["anti_cheat_passed"])

    def test_02_adversarial_post_lock_case_mutation_fails(self):
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
