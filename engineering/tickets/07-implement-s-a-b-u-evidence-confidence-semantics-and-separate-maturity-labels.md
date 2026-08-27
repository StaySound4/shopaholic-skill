# 07 — Implement S/A/B/U evidence-confidence semantics and separate maturity labels

**What to build:** Rate recommendation evidence coverage as S/A/B/U while giving products separate maturity states so confidence and market age are not conflated.

**Blocked by:** 06

**Status:** ready-for-agent

## Acceptance criteria

- [ ] S/A/B/U definitions operate on decision-critical claim coverage.
- [ ] Maturity labels are mature/conditional/watch/exclude.
- [ ] A new product may have strong short-term evidence but unverified long-term durability.
- [ ] No legacy A/B pool label is reused as evidence grade.

## Verification procedure

Pass: sparse new product becomes conditional with B/A as justified, not “B blackhorse” by taxonomy. Adversarial: mature/high-volume product with conflicting critical evidence cannot receive S merely because of age.

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
