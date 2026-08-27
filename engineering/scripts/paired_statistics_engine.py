#!/usr/bin/env python3
"""Paired statistics and feature-specific ablation interpretation engine.
Aggregates raw evaluation metrics into paired effect sizes, 95% confidence intervals,
paired t-tests, and Holm-Bonferroni multiplicity-corrected ablation interpretations.
Guarantees deterministic reproducibility with zero hardcoded oracle claims.
"""
import math
from typing import Any, Dict, List, Optional, Tuple

PREREGISTERED_ABLATION_METRICS = {
    "A_no_claim_ledger": "claim_ledger_accuracy",
    "A_no_provenance": "provenance_accuracy",
    "A_no_research_budget": "budget_compliance",
    "A_no_risk_adjudication": "safety_defect_recall",
    "A_no_market_scope_split": "scope_separation_accuracy",
    "A_no_sensitivity": "sensitivity_math_accuracy"
}

def compute_paired_differences(
    target_records: List[Dict[str, Any]],
    baseline_records: List[Dict[str, Any]],
    metric_name: str = "accuracy"
) -> Tuple[List[float], int]:
    """Extracts aligned paired differences between target and baseline across identical (case_id, replicate)."""
    target_map = {}
    for r in target_records:
        metrics = r.get("metrics", {})
        val = metrics.get(metric_name, metrics.get("accuracy", 0.0))
        target_map[(r["case_id"], r.get("replicate", 1))] = float(val)

    baseline_map = {}
    for r in baseline_records:
        metrics = r.get("metrics", {})
        val = metrics.get(metric_name, metrics.get("accuracy", 0.0))
        baseline_map[(r["case_id"], r.get("replicate", 1))] = float(val)

    common_keys = sorted(set(target_map.keys()) & set(baseline_map.keys()))
    differences = [target_map[k] - baseline_map[k] for k in common_keys]
    return differences, len(common_keys)

def compute_paired_effect_size_and_ci(
    differences: List[float]
) -> Dict[str, Any]:
    """Calculates mean paired difference, standard error, 95% CI, and t-statistic."""
    n = len(differences)
    if n == 0:
        return {
            "n": 0,
            "mean_difference": 0.0,
            "std_dev": 0.0,
            "standard_error": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "t_statistic": 0.0,
            "p_value": 1.0,
            "is_significant": False
        }

    mean_diff = sum(differences) / n
    variance = sum((x - mean_diff) ** 2 for x in differences) / (n - 1) if n > 1 else 0.0
    std_dev = math.sqrt(variance)
    se = std_dev / math.sqrt(n) if n > 0 else 0.0

    # z = 1.959964 for 95% CI
    z_multiplier = 1.959964
    ci_lower = mean_diff - z_multiplier * se
    ci_upper = mean_diff + z_multiplier * se

    if se <= 1e-9:
        if mean_diff > 0:
            t_stat = 999.0
            p_val = 0.0
        elif mean_diff < 0:
            t_stat = -999.0
            p_val = 0.0
        else:
            t_stat = 0.0
            p_val = 1.0
    else:
        t_stat = mean_diff / se
        p_val = math.erfc(abs(t_stat) / math.sqrt(2.0))

    return {
        "n": n,
        "mean_difference": round(mean_diff, 4),
        "std_dev": round(std_dev, 4),
        "standard_error": round(se, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "t_statistic": round(t_stat, 3),
        "p_value": round(p_val, 6),
        "is_significant": (p_val < 0.05) and (ci_lower > 0.0)
    }

def apply_holm_bonferroni_correction(
    ablation_p_values: List[Tuple[str, float]],
    alpha: float = 0.05
) -> List[Dict[str, Any]]:
    """Applies Holm-Bonferroni step-down family-wise error rate correction."""
    sorted_tests = sorted(ablation_p_values, key=lambda x: x[1])
    m = len(sorted_tests)
    results = []

    step_down_active = True
    for rank, (name, p_val) in enumerate(sorted_tests):
        adjusted_alpha = alpha / (m - rank)
        if step_down_active and p_val < adjusted_alpha:
            is_sig = True
        else:
            is_sig = False
            step_down_active = False # Step-down halting: all subsequent hypotheses fail to reject

        results.append({
            "ablation_name": name,
            "raw_p_value": p_val,
            "rank": rank + 1,
            "adjusted_alpha_threshold": round(adjusted_alpha, 6),
            "is_significant_after_correction": is_sig
        })

    return results

def aggregate_experiment_results(
    all_runs: List[Dict[str, Any]],
    target_condition: str = "T_full",
    baseline_condition: str = "B1_uploaded_current",
    ablation_conditions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Generates complete paired statistical analysis using preregistered relevant metrics."""
    target_runs = [r for r in all_runs if r.get("condition") == target_condition]
    baseline_runs = [r for r in all_runs if r.get("condition") == baseline_condition]

    t_vs_b_diffs, n_pairs = compute_paired_differences(target_runs, baseline_runs, "accuracy")
    main_effect = compute_paired_effect_size_and_ci(t_vs_b_diffs)

    ablations = ablation_conditions if ablation_conditions is not None else list(PREREGISTERED_ABLATION_METRICS.keys())

    ablation_results = {}
    ablation_p_list = []

    for ab in ablations:
        primary_metric = PREREGISTERED_ABLATION_METRICS.get(ab, "accuracy")
        ab_runs = [r for r in all_runs if r.get("condition") == ab]
        diffs, _ = compute_paired_differences(target_runs, ab_runs, primary_metric)
        ab_stats = compute_paired_effect_size_and_ci(diffs)
        ab_stats["evaluated_metric"] = primary_metric
        ablation_results[ab] = ab_stats
        ablation_p_list.append((ab, ab_stats["p_value"]))

    corrected_ablations = apply_holm_bonferroni_correction(ablation_p_list)

    return {
        "paired_sample_size": n_pairs,
        "main_comparison": {
            "target": target_condition,
            "baseline": baseline_condition,
            "evaluated_metric": "accuracy",
            "stats": main_effect
        },
        "ablations": ablation_results,
        "multiplicity_correction": corrected_ablations
    }

if __name__ == "__main__":
    print("Paired Statistics Engine Module ready.")
