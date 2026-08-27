# 31 — Build deterministic automated scorers for objective case assertions

**What to build:** Compute machine-checkable evaluation metrics from actual LLM run artifacts and case assertions (constraint violations, identity/SKU errors, price semantics, budget limits, round count, deterministic sensitivity math, standards errata, and dual-market certification unmasking), with zero pre-assigned condition scores.

**Blocked by:** 02, 04, 07, 08, 09, 10, 11, 13, 14, 18, 25, 30

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Scorer evaluates actual raw run artifacts (`run-record.schema.json`) with zero hardcoded condition-level score defaults.
- [ ] Per-assertion evidence includes exact failure reason, assertion type, and run/case ID.
- [ ] Verifies objective standard errata (IEEE 1789 vs 1788, GB 4706.1-2024 active status) and unmasks uncertified marketing claims (e.g. VESA HDR1000 verification).
- [ ] Known mutation fixtures and synthetic broken runs are reliably detected and penalized.
- [ ] Replicates aggregate without overwriting raw runs.
- [ ] Not-adjudicable / blocked states are strictly distinguished from passing scores.

## Verification procedure

Pass: run scorer on hand-constructed pass/fail fixtures including VESA HDR and standard errata assertions. Adversarial: an unknown gold field must not be scored as wrong.

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
