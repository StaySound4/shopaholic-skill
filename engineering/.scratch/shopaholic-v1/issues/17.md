# 17 — Make used/discontinued recommendations category-aware

**What to build:** Determine used eligibility and verification needs from hidden-history risk, safety, hygiene, support/EOL, battery/locks, inspectability, and product category.

**Blocked by:** 13, 16

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Camera/lens-style inspectable categories may admit used options.
- [ ] Safety-critical unknown-history products can be discouraged/restricted.
- [ ] Used checklist is category-specific.
- [ ] Old products include support/EOL/consumable compatibility in trade-off.

## Verification procedure

Pass: camera case may ask used; child-safety history-risk case does not treat used as ordinary value option. Adversarial: generic shutter-count checklist must not be applied to unrelated categories.

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
