# 02 — Define machine-readable evaluation cases and immutable manifests

**What to build:** Introduce versioned case and experiment contracts so a weak agent cannot change prompts, assertions, gates, or conditions after seeing target outputs without creating a new experiment version.

**Blocked by:** 01

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Every case has stable ID/version/tier/prompt/assertions.
- [ ] Experiment manifest stores case-set hash, conditions, replicates, seed, model/runtime and release gates.
- [ ] Changing a case changes the case-set hash.
- [ ] A preregistered manifest cannot be mutated without a new experiment ID.

## Verification procedure

Validate at least 40 seed cases; mutate one prompt byte and show case-set hash changes. Adversarial: attempt to reuse a preregistered manifest with the changed case set and require INVALID_PROTOCOL.

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
