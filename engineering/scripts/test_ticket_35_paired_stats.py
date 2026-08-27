#!/usr/bin/env python3
"""Test suite for Ticket 35: Compute paired statistics and feature-specific ablation interpretations.
Tests:
1. Pass: Paired differences, effect size, 95% CI, and Holm-Bonferroni multiplicity corrections on preregistered metrics.
2. Pass: Step-down termination rule in Holm-Bonferroni halts significance when early rank fails.
3. Pass: Zero-variance negative difference evaluates to extreme negative t-stat and near-zero p-value.
4. Adversarial: Shuffling condition labels changes mean effect and inverts conclusion.
5. Adversarial: Unpaired cases correctly decrease the paired sample size.
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
            # Target has higher accuracy across all metrics
            self.runs.append({
                "case_id": cid, "condition": "T_full", "replicate": 1,
                "metrics": {
                    "accuracy": 0.90,
                    "claim_ledger_accuracy": 0.95,
                    "provenance_accuracy": 0.90,
                    "budget_compliance": 1.0,
                    "safety_defect_recall": 1.0,
                    "scope_separation_accuracy": 0.90,
                    "sensitivity_math_accuracy": 0.95
                }
            })
            # Baseline
            self.runs.append({
                "case_id": cid, "condition": "B1_uploaded_current", "replicate": 1,
                "metrics": {"accuracy": 0.60}
            })
            # Ablations with distinct feature-specific metric degradations
            ab_map = {
                "A_no_claim_ledger": {"claim_ledger_accuracy": 0.50},
                "A_no_provenance": {"provenance_accuracy": 0.40},
                "A_no_research_budget": {"budget_compliance": 0.60},
                "A_no_risk_adjudication": {"safety_defect_recall": 0.30},
                "A_no_market_scope_split": {"scope_separation_accuracy": 0.50},
                "A_no_sensitivity": {"sensitivity_math_accuracy": 0.20}
            }
            for ab, mdict in ab_map.items():
                self.runs.append({"case_id": cid, "condition": ab, "replicate": 1, "metrics": mdict})

    def test_01_paired_statistics_and_preregistered_metrics(self):
        """Pass path: Verify paired sample size, mean delta (+0.30), 95% CI, and ablation metric routing."""
        report = aggregate_experiment_results(self.runs)
        
        self.assertEqual(report["paired_sample_size"], 20)
        main = report["main_comparison"]["stats"]
        self.assertEqual(main["mean_difference"], 0.30)
        self.assertTrue(main["ci_lower"] > 0.0)
        self.assertTrue(main["is_significant"])

        # Check that ablations used their primary metric
        self.assertEqual(report["ablations"]["A_no_sensitivity"]["evaluated_metric"], "sensitivity_math_accuracy")
        self.assertEqual(report["ablations"]["A_no_provenance"]["evaluated_metric"], "provenance_accuracy")

    def test_02_holm_bonferroni_step_down_halting(self):
        """Pass path: Holm-Bonferroni halts on first non-significant rank."""
        # Rank 1: p=0.010 < 0.05/3 (0.0167) -> True
        # Rank 2: p=0.030 >= 0.05/2 (0.0250) -> False (Halts)
        # Rank 3: p=0.040 (would be < 0.05/1 if independent, but halts because rank 2 failed -> False)
        tests = [("A1", 0.010), ("A2", 0.030), ("A3", 0.040)]
        res = apply_holm_bonferroni_correction(tests, alpha=0.05)
        
        self.assertTrue(res[0]["is_significant_after_correction"])
        self.assertFalse(res[1]["is_significant_after_correction"])
        self.assertFalse(res[2]["is_significant_after_correction"]) # Halting enforced

    def test_03_zero_variance_negative_difference(self):
        """Pass path: Zero-variance negative delta yields negative t-stat and near-zero p-value."""
        diffs = [-0.25] * 10
        stats = compute_paired_effect_size_and_ci(diffs)
        self.assertEqual(stats["mean_difference"], -0.25)
        self.assertEqual(stats["t_statistic"], -999.0)
        self.assertEqual(stats["p_value"], 0.0)
        self.assertFalse(stats["is_significant"])

    def test_04_adversarial_shuffled_labels_invert_conclusion(self):
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

    def test_05_adversarial_unpaired_cases_reduce_n(self):
        """Adversarial path: Dropping half the baseline runs accurately reduces paired sample size."""
        partial_runs = [r for r in self.runs if not (r["condition"] == "B1_uploaded_current" and int(r["case_id"][-2:]) > 10)]
        report = aggregate_experiment_results(partial_runs)
        self.assertEqual(report["paired_sample_size"], 10)

if __name__ == "__main__":
    unittest.main()
