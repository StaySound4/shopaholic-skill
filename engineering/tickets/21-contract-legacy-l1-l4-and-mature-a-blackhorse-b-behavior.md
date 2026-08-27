# 21 — Contract legacy L1-L4 and mature-A/blackhorse-B behavior

**What to build:** Remove or neutralize legacy taxonomies and fixed quotas after new evidence/output behavior reaches regression parity.

**Blocked by:** 07, 20

**Status:** ready-for-agent

## Acceptance criteria

- [ ] No normative fixed 8/10 source quota remains.
- [ ] No normative 10-15/6-10 candidate quota remains.
- [ ] No user-facing L1-L4 hierarchy remains.
- [ ] Maturity and evidence grade cannot collide on A/B labels; legacy `candidate_pools.tier_a_mature/tier_b_observation` fields are completely migrated to 4 explicit pools (`mature_recommendations`, `conditional_recommendations`, `watch_list`, `excluded`).
## Verification procedure

Run legacy regression cases before/after contraction. Adversarial: grep/static audit must catch remaining normative quota phrases and fixed-year examples presented as rules.

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
