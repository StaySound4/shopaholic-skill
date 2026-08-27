# 10 — Add origin and temporal semantics without inference shortcuts

**What to build:** Separate origin/assembly, regulatory standard status (`active`, `upcoming`, `superseded`, `repealed`), and announcement/first-sale/regional-sale/certification/revision/batch/EOL dates, with explicit inference prohibitions.

**Blocked by:** 08, 09

**Status:** ready-for-agent

## Acceptance criteria

- [ ] GTIN licence country does not imply origin or manufacturing plant.
- [ ] Company nationality does not imply assembly/manufacture origin.
- [ ] Regulatory standard status (`active`, `upcoming`, `superseded`, `repealed`) is strictly verified rather than assumed from static memory.
- [ ] Certification date is distinct from first-sale and regional release dates.
- [ ] Batch launch window (`batch_window`) is explicitly distinguished from model release date.
- [ ] Runtime current-year queries derive dynamically from runtime date.

## Verification procedure

Pass: certification Jan, announcement Mar, sale Mar10 stay separate; 2031 runtime uses 2031 current anchors; standard status is verified against registry. Adversarial: German GTIN license party with no factory evidence must not become “Made in Germany”.

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
