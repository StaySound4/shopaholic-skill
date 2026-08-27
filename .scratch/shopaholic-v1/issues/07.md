# 07 — Implement S/A/B/U evidence-confidence semantics and separate maturity labels

**What to build:** Rate recommendation evidence coverage as S/A/B/U while giving products separate maturity states so confidence and market age are not conflated.

**Blocked by:** 06

**Status:** completed

## Acceptance criteria

- [x] S/A/B/U definitions operate on decision-critical claim coverage.
- [x] Maturity labels are mature/conditional/watch/exclude.
- [x] A new product may have strong short-term evidence but unverified long-term durability.
- [x] No legacy A/B pool label is reused as evidence grade.

## Verification procedure

Pass: sparse new product becomes conditional with B/A as justified, not “B blackhorse” by taxonomy. Adversarial: mature/high-volume product with conflicting critical evidence cannot receive S merely because of age.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- **Verification command**: `python engineering/scripts/test_ticket_07_confidence_maturity.py` -> 3 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/evidence_confidence_engine.py`, `engineering/scripts/test_ticket_07_confidence_maturity.py`.
- **Adversarial check**: Mature popular product with disputed claims cannot receive Grade S (0% bypass).
- **Limitations**: None. Evidence confidence (S/A/B/U) and maturity pool separation operational.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
