#!/usr/bin/env python3
"""Test suite for Ticket 35: Compute paired statistics and feature-specific ablation interpretations.
Tests:
1. Pass: Paired differences, effect size, 95% CI, and Holm-Bonferroni multiplicity corrections calculated deterministically.
2. Adversarial: Shuffling condition labels changes mean effect and inverts conclusion.
3. Adversarial: Unpaired cases correctly decrease the paired sample size.
"""
import unittest, sys, copy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paired_statistics_engine import (
    compute_paired_differences,
    compute_paired_effect_size_and_ci,
    apply_holm_bonferroni_correction,
    aggregate_experiment_results
)

class TestTicket35PairedStats(unittest.TestCase):
    def setUp(self):
        self.runs = []
        # Generate 20 paired cases
        for i in range(20):
            cid = f"CASE-{i+1:02d}"
            # Target has higher accuracy (0.90)
            self.runs.append({"case_id": cid, "condition": "T_full", "replicate": 1, "metrics": {"accuracy": 0.90}})
            # Baseline has lower accuracy (0.60)
            self.runs.append({"case_id": cid, "condition": "B1_uploaded_current", "replicate": 1, "metrics": {"accuracy": 0.60}})
            # Ablations
            for ab in ["A_no_claim_ledger", "A_no_provenance", "A_no_research_budget",
                       "A_no_risk_adjudication", "A_no_market_scope_split", "A_no_sensitivity"]:
                self.runs.append({"case_id": cid, "condition": ab, "replicate": 1, "metrics": {"accuracy": 0.75}})

    def test_01_paired_statistics_and_ci_calculation(self):
        """Pass path: Verify paired sample size, mean delta (+0.30), 95% CI, and Holm-Bonferroni correction."""
        report = aggregate_experiment_results(self.runs)
        
        self.assertEqual(report["paired_sample_size"], 20)
        main = report["main_comparison"]["stats"]
        self.assertEqual(main["mean_difference"], 0.30)
        self.assertTrue(main["ci_lower"] > 0.0)
        self.assertTrue(main["is_significant"])

        # Check multiplicity corrections
        mult = report["multiplicity_correction"]
        self.assertEqual(len(mult), 6)
        for row in mult:
            self.assertIn("adjusted_alpha_threshold", row)
            self.assertIn("is_significant_after_correction", row)

    def test_02_adversarial_shuffled_labels_invert_conclusion(self):
        """Adversarial path: Shuffling condition labels inverts mean delta and alters conclusions."""
        shuffled_runs = copy.deepcopy(self.runs)
        for r in shuffled_runs:
            if r["condition"] == "T_full":
                r["condition"] = "B1_uploaded_current"
            elif r["condition"] == "B1_uploaded_current":
                r["condition"] = "T_full"

        report = aggregate_experiment_results(shuffled_runs)
        main = report["main_comparison"]["stats"]
        self.assertEqual(main["mean_difference"], -0.30)
        self.assertFalse(main["is_significant"])

    def test_03_adversarial_unpaired_cases_reduce_n(self):
        """Adversarial path: Dropping half the baseline runs accurately reduces paired sample size."""
        partial_runs = [r for r in self.runs if not (r["condition"] == "B1_uploaded_current" and int(r["case_id"][-2:]) > 10)]
        report = aggregate_experiment_results(partial_runs)
        self.assertEqual(report["paired_sample_size"], 10)

if __name__ == "__main__":
    unittest.main()
