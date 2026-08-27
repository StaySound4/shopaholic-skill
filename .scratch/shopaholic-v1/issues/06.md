# 06 — Replace universal L1-L4 truth ranking with claim-specific evidence roles

**What to build:** Route sources by what they can prove: regulatory compliance (CCC, UL, CE, FDA), voluntary gold-standard certifications (TÜV, VESA DisplayHDR, OEKO-TEX, ECE R129, LFGB), official primary specifications, independent lab measurements (RTINGS, LTT Labs), field/repair data, corporate registries, and market/price.

**Blocked by:** 05

**Status:** completed

## Acceptance criteria

- [x] Source role is stored independently from claim confidence.
- [x] Regulatory and voluntary certifications (CCC, UL, CE, TÜV, VESA, OEKO-TEX) support legal market entry or certified technical capabilities, but do not alone prove unmeasured long-term durability.
- [x] Seller price is valid market evidence but not durability evidence.
- [x] Official spec can strongly support declared dimensions/interfaces without proving superiority over competitors.
- [x] No fixed source-count requirement determines confidence.

## Verification procedure

Pass: seller offer supports price; official manual supports feature; VESA registry supports DisplayHDR tier; independent lab supports measured performance. Adversarial: ten seller pages asserting durability cannot upgrade a high-impact comparative claim to verified.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- Raw unedited output(s).
- **Verification command**: `python engineering/scripts/test_ticket_06_evidence_roles.py` -> 3 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/evidence_role_router.py`, `engineering/scripts/test_ticket_06_evidence_roles.py`.
- **Adversarial check**: 10 seller marketing pages claiming durability cannot verify a durability claim (0% bypass rate).
- **Limitations**: None. Claim-specific evidence role routing operational.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
