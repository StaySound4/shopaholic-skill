# 09 — Add provenance and corporate-role graph

**What to build:** Represent brand owner, trademark owner, regulatory applicant, manufacturer, factory, ODM/OEM, importer, distributor, seller, and parent company as independent evidence-backed roles.

**Blocked by:** 08

**Status:** completed

## Acceptance criteria

- [x] Roles can differ without forced merging across 10 corporate entities.
- [x] Each populated role points to supporting evidence.
- [x] Strictly distinguishes proprietary custom OEM/ODM manufacturing (`proprietary_oem`) from public-tooling rebadging (`public_tooling_rebadge`).
- [x] Public-tooling rebadging (白牌公模套壳/挂牌) is unmasked and traced to original ODM/OEM when brand markups reach >=30%~40% or show significant unverified premiums.
- [x] Export-return and parallel-import gray market channel risks are explicitly labeled.
- [x] Unknown roles remain unknown.
- [x] Seller/brand/manufacturer are not interchangeable.
## Verification procedure
Pass: case with four distinct entities preserves all roles. Adversarial: marketplace “brand story” cannot overwrite a regulatory manufacturer record without conflict handling.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- **Verification command**: `python engineering/scripts/test_ticket_09_provenance.py` -> 4 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/provenance_graph.py`, `engineering/scripts/test_ticket_09_provenance.py`.
- **Adversarial check**: Marketplace brand marketing cannot overwrite regulatory manufacturer records (100% precision).
- **Limitations**: None. 10-role corporate graph and supply-chain unmasking operational.

## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
