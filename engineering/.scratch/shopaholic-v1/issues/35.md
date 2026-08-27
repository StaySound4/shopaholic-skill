# 35 — Compute paired statistics and feature-specific ablation interpretations

**What to build:** Aggregate real run metrics into paired effect sizes, confidence intervals, appropriate paired tests, and corrected feature-specific ablation claims.

**Blocked by:** 34

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Baseline/target paired sample sizes are explicit.
- [ ] Effect size and 95% CI reported.
- [ ] Ablation conclusion uses preregistered relevant metrics only.
- [ ] Multiplicity correction used for confirmatory multiple ablations.
- [ ] No hard-coded oracle claims.

## Verification procedure

Recompute report from raw annotation metrics and verify deterministic reproducibility. Adversarial: shuffle condition labels or remove paired cases and ensure analysis detects mismatch rather than producing the same conclusion.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- Raw unedited output(s).
- Structured artifact(s) produced by this ticket when applicable.
- Scorer/test output with command or reproducible invocation.
- Source snapshot/locator and access status for evidence-dependent checks.
- Short limitations/blockers note, even when all criteria pass.

## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
