# 03 — Add evaluator positive and sham controls

**What to build:** Make evaluator validity measurable by adding a deliberately bad-evidence condition and a presentation-only sham condition before interpreting target improvements.

**Blocked by:** 02

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Positive control intentionally introduces unsupported/role-mismatched claims.
- [ ] Sham changes presentation without improving decision logic.
- [ ] Protocol states expected control behavior before runs.
- [ ] Control failure invalidates confirmatory interpretation.

## Verification procedure

Run a small controlled subset across baseline/positive-control/sham. Positive control must worsen evidence/correctness metrics; sham must not gain correctness merely from style. Adversarial: use a presentation-biased rubric and verify the sham-control check exposes it.

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
