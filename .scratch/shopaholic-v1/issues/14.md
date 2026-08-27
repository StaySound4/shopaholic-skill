# 14 — Separate global evidence scope from purchase and output market scope

**What to build:** Support evidence_scope, purchase_scope and output_scope independently so global compliance registries and lab verifications (FCC, EPREL, FDA, UL, CE, VESA, TÜV, RTINGS) can verify product claims without leaking foreign purchase candidates into a China-only request, while cross-verifying dual-market global models.

**Blocked by:** 08, 10

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Default evidence scope is global across international standard and regulatory registries.
- [ ] Purchase scope is cn/overseas/both.
- [ ] Output scope is cn/overseas/combined.
- [ ] Overseas-only product is excluded from China-only purchase output even if used as evidence.
- [ ] Global regulatory filings (e.g. FCC ID internal photos, EPREL energy logs) are cross-checked against domestic claims to expose component downgrades and uncertified marketing claims (e.g. unverified HDR1000).

## Verification procedure

Pass: China-only case consults overseas regulatory source and VESA registry but recommends only China-purchasable SKU. Adversarial: global evidence lookup must not silently set purchase_scope=both.

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
