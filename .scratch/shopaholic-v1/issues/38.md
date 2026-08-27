# 38 — Govern community category contributions

**What to build:** Create category contribution, automated linting, and anti-PR review rules requiring strict compliance with `CATEGORY_CONTRIBUTION_TEMPLATE.md`, mandatory domestic and international standards/certifications coverage (e.g. CCC, UL, CE, TÜV, VESA, OEKO-TEX, ECE R129, GB 4806, FDA), commercial conflict disclosures, falsifiable counterexamples, automated static playbook linting (`validate_category_playbook.py`), and zero contributor reputation shortcuts.

**Blocked by:** 27, 33, 36

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Community contributions must strictly follow the 12-section `CATEGORY_CONTRIBUTION_TEMPLATE.md` structure.
- [ ] Category playbooks must define relevant domestic (CCC, GB) and international (UL, CE, TÜV, VESA, OEKO-TEX, ECE) standards and certification registries where applicable.
- [ ] Automated playbook linter (`engineering/scripts/validate_category_playbook.py`) verifies section completeness, valid markdown structure, and required metadata.
- [ ] Commercial relationships, sponsorships, and affiliations must be explicitly declared; missing disclosure triggers rejection.
- [ ] Falsifiable counterexamples and boundary limits are mandatory for every decision heuristic.
- [ ] Static transient facts (hardcoded prices, active top-10 lists) are forbidden from merging without explicit runtime verification anchors and expiry dates.
- [ ] Reviewer ownership and last-reviewed timestamp are recorded for every playbook.
- [ ] No contributor reputation or KOL status bypasses automated linting and empirical evidence checks.
- [ ] Contribution rejection criteria and automated linter errors provide clear, actionable remediation guidance.

## Verification procedure

Pass: valid new playbook passing all 12 sections, standards coverage, and linter checks merges cleanly. Adversarial: a PR with omitted commercial disclosure, missing standard registries, unverified hardcoded prices, or missing counterexamples is automatically rejected by the playbook linter.

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
