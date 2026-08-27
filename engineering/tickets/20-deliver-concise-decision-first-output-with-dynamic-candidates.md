# 20 — Deliver concise decision-first output with dynamic candidates

**What to build:** Replace mandatory giant matrix bloat with a compact decision-first answer that adapts to user preference, supports extreme 1-candidate compression on demand ("just tell me which one to buy"), and scales candidate counts dynamically.

**Blocked by:** 07, 12, 17, 18, 19, 24, 25, 26

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Decision and recommended candidate appear before lengthy methodology.
- [ ] Candidate count follows survivors dynamically (0, 1, 2, or 3+), not artificial quotas.
- [ ] When user requests extreme brevity ("direct recommendation" / "just tell me which one"), system outputs a single decisive choice without bloated matrices.
- [ ] Default table contains only decision-relevant fields; empty columns and synthetic BOM padding are forbidden.
- [ ] Broad search flagship knowledge is strictly used for factual compromise attribution within budget, never for recommending out-of-budget picks or patronizing the buyer.
- [ ] Deep provenance and evidence traces remain accessible on demand without cluttering the primary answer, enclosing the structured Decision Record within a single `<decision_record>...</decision_record>` XML block in benchmark evaluation runs.
## Verification procedure

Pass: "just tell me what to buy" produces single decisive top choice; three viable candidates produce compact 3-row comparison. Adversarial: outputting an empty column or 10-row matrix for a trivial 60-yuan purchase fails the concise delivery check.

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
