# 19 — Add cross-border landed-cost and compatibility treatment

**What to build:** When overseas purchasing is allowed, compare explicit landed monetary cost assumptions, verify destination legal certifications (UL/CSA, CE DoC, PSE, FDA, EPREL), and separately disclose non-monetary regional risks (missing domestic 3C, voltage/plug incompatibility, voided domestic warranty).

**Blocked by:** 14, 18

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Known product+shipping+tax+FX arithmetic is deterministic.
- [ ] Unknown shipping/tax is a range/unknown, not invented exact.
- [ ] Warranty void, voltage/plug (110V/220V), lack of domestic 3C, regional cloud locks, legality, return friction are explicitly disclosed.
- [ ] Destination electrical and safety certifications (UL, ETL, CSA, CE, PSE) are verified for overseas candidates.
- [ ] Sticker-price-only ranking is forbidden when landed costs materially differ.
- [ ] Amazon/overseas seller tiers (`Sold & Shipped by Retailer` vs `FBA` vs `FBM`) are explicitly labeled.
- [ ] Overseas historical price tracking (Keepa / CamelCamelCamel logic) unmasks inflated list prices and deal markups.
- [ ] Review hijacking (ASIN variation swapping) and unverified reviews are filtered.
- [ ] Refurbished/open-box condition (`Amazon Renewed`, `Warehouse Deals`) is distinguished from brand new.

## Verification procedure

Pass: $500+$30+$50 at 7.00 produces CNY4060. Adversarial: unknown tax cannot be silently set to zero.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

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
