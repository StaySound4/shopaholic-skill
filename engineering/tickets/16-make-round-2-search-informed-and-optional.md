# 16 — Make Round 2 search-informed and optional

**What to build:** After initial research, ask only questions whose answers would materially change the survivor set or ranking; eradicate layout format questioning, restrict used-goods questions to category-eligible contexts, and skip Round 2 when inputs are already sufficient.

**Blocked by:** 12, 15

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Every Round 2 question has an identified decision consequence.
- [ ] Layout and format questions (e.g. asking the user to pick dual-track vs scenario matrix) are strictly forbidden.
- [ ] Used-goods questions are category-aware (never asked for hygiene/food/safety categories; only asked when inspectable and high-value discontinued flagships are discovered).
- [ ] Questions already answered or non-material boundaries result in skipping Round 2 directly to delivery.

## Verification procedure

Pass: search finds used camera flagship at same price and asks used acceptance; baby car seat query skips used questions; clear request skips Round 2 entirely. Adversarial: asking the user for matrix format preferences triggers failure.
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
