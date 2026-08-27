# 04 — Replace H/S with three constraint classes

**What to build:** Support safety/compatibility hard constraints, user-declared hard constraints, and soft preferences as distinct decision inputs, enforcing strict candidate exclusion in final delivery while allowing broad search exploration (+30%~50% budget headroom) for category knowledge grounding.

**Blocked by:** 01

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Both hard classes (`safety_compatibility_hard` and `user_declared_hard`) can strictly exclude candidates from the final recommendation.
- [ ] Explicit budget caps, brand exclusions, no-used requirements, and ecosystem dependencies are categorized as user hard constraints.
- [ ] Soft preferences rank candidates on the Pareto frontier but do not masquerade as physical impossibility.
- [ ] Broad search exploration is decoupled from candidate exclusion: searching high-tier/over-budget items for domain physics grounding does not violate user hard constraints.
- [ ] Constraint class and exclusion reason are observable in the Decision Record.

## Verification procedure

Pass: budget<=3000 strictly excludes 3299 from final recommended picks; broad search ingests 4500 flagship physics to explain 3000 compromises; must-HomeKit does not assume unsupported compatibility. Adversarial: color preference alone must not be classified as safety incompatibility.

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
