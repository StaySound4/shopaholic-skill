# 34 — Run the first real paired baseline/full/ablation experiment

**What to build:** Execute real LLM inference across preregistered baseline (`B0_no_skill`, `B1_uploaded_current`), target (`T_full`), 6 feature ablations (`A_no_*`), and 2 anti-cheat controls (`C_positive_bad_evidence`, `C_sham_style`) on the fixed case set, storing unedited raw run logs.

**Blocked by:** 03, 20, 21, 23, 25, 28, 29, 30, 31, 32, 33

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Experiment manifest (`experiment-manifest.schema.json`) is preregistered and hash-locked before target runs commence.
- [ ] Every planned run generates a real, unedited raw output artifact (`run-record.schema.json`).
- [ ] Both anti-cheat controls (`C_positive_bad_evidence` and `C_sham_style`) are evaluated to confirm evaluator validity before target claims are interpreted.
- [ ] Absolutely no manual output repair or cherry-picking of runs.
- [ ] Blocked, failed, and invalid runs are accounted for and reported separately.
## Verification procedure

Run at least the smoke set first, then the preregistered beta-size set when implementation is ready. Adversarial: changing a case after target output invalidates old manifest rather than silently continuing.

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
