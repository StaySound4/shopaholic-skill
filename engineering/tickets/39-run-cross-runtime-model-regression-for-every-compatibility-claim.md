# 39 — Run cross-runtime/model regression for every compatibility claim

**What to build:** Measure critical behavioral seams across each runtime/model combination the project publicly claims, recording capability blocks separately from behavior failures.

**Blocked by:** 30, 36, 37

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Each public compatibility claim maps to at least one tested configuration.
- [ ] Critical constraints/evidence/security cases run across configurations.
- [ ] Capability gaps are explicit.
- [ ] No runtime result is generalized to untested runtimes.

## Verification procedure

Run a minimal critical suite on each claimed runtime/model. Adversarial: remove a required tool in one runtime and verify it is reported as capability/degraded difference, not hidden.

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
