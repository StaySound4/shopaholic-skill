# 06 — Replace universal L1-L4 truth ranking with claim-specific evidence roles

**What to build:** Route sources by what they can prove: regulatory compliance (CCC, UL, CE, FDA), voluntary gold-standard certifications (TÜV, VESA DisplayHDR, OEKO-TEX, ECE R129, LFGB), official primary specifications, independent lab measurements (RTINGS, LTT Labs), field/repair data, corporate registries, and market/price.

**Blocked by:** 05

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Source role is stored independently from claim confidence.
- [ ] Regulatory and voluntary certifications (CCC, UL, CE, TÜV, VESA, OEKO-TEX) support legal market entry or certified technical capabilities, but do not alone prove unmeasured long-term durability.
- [ ] Seller price is valid market evidence but not durability evidence.
- [ ] Official spec can strongly support declared dimensions/interfaces without proving superiority over competitors.
- [ ] No fixed source-count requirement determines confidence.

## Verification procedure

Pass: seller offer supports price; official manual supports feature; VESA registry supports DisplayHDR tier; independent lab supports measured performance. Adversarial: ten seller pages asserting durability cannot upgrade a high-impact comparative claim to verified.

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
