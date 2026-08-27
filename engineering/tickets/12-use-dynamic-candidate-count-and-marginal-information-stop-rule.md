# 12 — Use dynamic candidate count and marginal-information stop rule

**What to build:** Replace fixed 3+2+1, 10-15 discovery, and 6-10 final quotas with a stop rule based on decision-relevant information gain.

**Blocked by:** 06, 11

**Status:** ready-for-agent

## Acceptance criteria

- [ ] No candidate minimum forces padding.
- [ ] Discovery tracks new technology route, identity correction, safety finding, Pareto candidate, or value frontier.
- [ ] Two no-gain passes may stop when no critical claim remains unresolved.
- [ ] Final can contain 0, 2, 3, or more justified candidates.

## Verification procedure

Pass: case with only three viable products outputs three. Adversarial: repeating synonym searches that add no new route cannot extend research just to meet a count.

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
