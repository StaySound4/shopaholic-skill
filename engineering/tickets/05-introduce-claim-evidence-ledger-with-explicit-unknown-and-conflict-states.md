# 05 — Introduce claim/evidence ledger with explicit unknown and conflict states

**What to build:** Make decision-critical claims first-class records with scope, impact, evidence references, status, and the ability to remain disputed or unverified.

**Blocked by:** 01

**Status:** completed

## Acceptance criteria

- [x] High-impact claims can be verified/disputed/unverified.
- [x] Claims are scoped to product/region/revision/batch.
- [x] Contradicting evidence is preserved.
- [x] Missing evidence is represented, never filled to satisfy an output template.
- [x] Claim-Metric Discrepancy (CMD / 宣称-实测偏差) is structured as an explicit pairing of claimed specification vs independent lab measurement, capturing deviation type and severity.
## Verification procedure

Pass: official 500g vs independent 535g yields a disputed weight claim. Adversarial: a new-product long-term durability claim with no long-term evidence must remain unverified.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- **Verification command**: `python engineering/scripts/test_ticket_05_claim_ledger.py` -> 3 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/claim_ledger.py`, `engineering/scripts/test_ticket_05_claim_ledger.py`.
- **Adversarial check**: New-product durability claims lacking long-term evidence remain unverified (grade U) with 100% precision.
- **Limitations**: None. Claim-evidence ledger operational.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
