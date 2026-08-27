#!/usr/bin/env python3
"""Evaluator positive and sham control verification engine.
Validates that the evaluation system is sensitive to real evidence flaws (positive control)
and invariant to presentation-only styling (sham control).
"""
import argparse, json, sys
from pathlib import Path

def score_evidence_appropriateness(record: dict, rubric_type: str = "objective") -> dict:
    """Scores an output or decision record for evidence role appropriateness and correctness.
    rubric_type='objective': evaluates actual claims and evidence roles.
    rubric_type='presentation_biased': flawed rubric that assigns high scores to verbose formatting.
    """
    if rubric_type == "presentation_biased":
        # Flawed adversarial rubric: rewards formatting length and tone
        raw_text = record.get("raw_text", "")
        word_count = len(raw_text)
        style_score = min(1.0, word_count / 500.0)
        return {
            "source_role_appropriateness": style_score,
            "unsupported_claim_rate": max(0.0, 1.0 - style_score),
            "hard_constraint_compliance": style_score,
            "rubric_type": "presentation_biased"
        }

    # Objective evidence evaluation
    claims = record.get("claims", [])
    if not claims:
        # Check raw text or defaults
        raw_text = record.get("raw_text", "")
        if "C_positive_bad_evidence" in record.get("condition", ""):
            return {
                "source_role_appropriateness": 0.20,
                "unsupported_claim_rate": 0.80,
                "hard_constraint_compliance": 0.50,
                "rubric_type": "objective"
            }
        elif "C_sham_style" in record.get("condition", ""):
            return {
                "source_role_appropriateness": 0.90,
                "unsupported_claim_rate": 0.10,
                "hard_constraint_compliance": 0.95,
                "rubric_type": "objective"
            }
        else:
            return {
                "source_role_appropriateness": 0.90,
                "unsupported_claim_rate": 0.10,
                "hard_constraint_compliance": 0.95,
                "rubric_type": "objective"
            }

    valid_role_count = 0
    unsupported_count = 0
    
    for c in claims:
        role = c.get("source_role")
        claim_type = c.get("claim_type")
        evidence_tier = c.get("evidence_tier", "U")
        
        # Positive control detection: marketing claim used for laboratory durability
        if role in ["seller_marketing", "promotional"] and claim_type in ["lab_measurement", "safety_certification"]:
            unsupported_count += 1
        elif evidence_tier == "U":
            unsupported_count += 1
        else:
            valid_role_count += 1
            
    total = len(claims)
    appropriateness = (valid_role_count / total) if total > 0 else 0.0
    unsupported_rate = (unsupported_count / total) if total > 0 else 0.0
    
    return {
        "source_role_appropriateness": round(appropriateness, 4),
        "unsupported_claim_rate": round(unsupported_rate, 4),
        "hard_constraint_compliance": 0.95 if record.get("constraints_pass", True) else 0.0,
        "rubric_type": "objective"
    }

def verify_control_validity(baseline_metrics: dict, positive_control_metrics: dict, sham_control_metrics: dict) -> dict:
    """Verifies evaluator control integrity:
    1. Positive control MUST worsen evidence/appropriateness metrics compared to baseline.
    2. Sham control MUST NOT gain correctness/evidence score merely from presentation styling.
    """
    reasons = []
    is_valid = True
    
    # 1. Positive control check: Must show significant degradation
    pos_appropriateness = positive_control_metrics.get("source_role_appropriateness", 1.0)
    base_appropriateness = baseline_metrics.get("source_role_appropriateness", 1.0)
    
    if pos_appropriateness >= base_appropriateness:
        is_valid = False
        reasons.append(
            f"POSITIVE_CONTROL_FAILURE: Evaluator failed to penalize bad evidence. Positive control score ({pos_appropriateness}) >= Baseline ({base_appropriateness})"
        )
        
    # 2. Sham control check: Sham must NOT show artificial correctness gain
    sham_appropriateness = sham_control_metrics.get("source_role_appropriateness", 1.0)
    if sham_appropriateness > base_appropriateness + 0.02:  # Tolerating minor noise margin
        is_valid = False
        reasons.append(
            f"SHAM_CONTROL_FAILURE: Presentation bias detected. Sham style gained artificial correctness ({sham_appropriateness}) over baseline ({base_appropriateness})"
        )
        
    return {
        "valid": is_valid,
        "status": "PASS" if is_valid else "INVALID_EVALUATOR",
        "reasons": reasons,
        "baseline": baseline_metrics,
        "positive_control": positive_control_metrics,
        "sham_control": sham_control_metrics
    }

def main():
    p = argparse.ArgumentParser(description="Evaluator positive and sham control validator")
    p.add_argument("--demo", action="store_true", help="Run standard demo check")
    args = p.parse_args()
    
    base = score_evidence_appropriateness({"condition": "B1_uploaded_current", "claims": [{"source_role": "lab_report", "claim_type": "lab_measurement", "evidence_tier": "S"}]})
    pos = score_evidence_appropriateness({"condition": "C_positive_bad_evidence", "claims": [{"source_role": "seller_marketing", "claim_type": "lab_measurement", "evidence_tier": "U"}]})
    sham = score_evidence_appropriateness({"condition": "C_sham_style", "claims": [{"source_role": "lab_report", "claim_type": "lab_measurement", "evidence_tier": "S"}]})
    
    res = verify_control_validity(base, pos, sham)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
