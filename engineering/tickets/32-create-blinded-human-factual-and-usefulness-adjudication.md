# 32 — Create blinded human factual and usefulness adjudication

**What to build:** Define reproducible human-review packets, independent reviewers, adjudication, randomized pairwise presentation, and inter-rater agreement reporting.

**Blocked by:** 02, 05, 31

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Condition labels are hidden from reviewers.
- [ ] Pairwise left/right order is randomized.
- [ ] Two independent reviewers cover factual/safety holdout.
- [ ] Disagreement is adjudicated and preserved.
- [ ] Presentation cannot override correctness priority.

## Verification procedure

Pilot at least 10 pairs. Adversarial: swap answer order and confirm rubric result is not systematically position-dependent; run sham control to expose presentation bias.

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
