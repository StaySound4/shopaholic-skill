# 08 — Resolve Canonical Product, Region SKU, Revision, and Batch

**What to build:** Create the product-identity hierarchy (`Canonical Product -> Region SKU -> Revision -> Batch`), link Region SKUs to jurisdiction-specific compliance identifiers (China 3C/CEL, US FCC ID/UL, EU CE/EPREL, Japan PSE), and ensure claim scope follows the narrowest evidence-supported identity.

**Blocked by:** 05

**Status:** completed

## Acceptance criteria

- [x] Bundle/accessory SKUs can map to one canonical host product.
- [x] Region variants remain distinct when decision-relevant properties (voltage 110V/220V, certification, warranty) differ.
- [x] Region SKUs record jurisdiction compliance identifiers (3C, FCC ID, EPREL, UL, PSE) and structured certifications.
- [x] Revision and batch can be represented independently.
- [x] Batch recommendation provides launch window and physical SN/nameplate verification method.
- [x] Unknown lower-level identity is not guessed.

## Verification procedure

Pass: same main-unit GTIN in different bundles resolves one canonical product; CN (3C/220V) and US (FCC/UL/120V) variants remain distinct. Adversarial: a revision with changed interface cannot inherit old-revision feature claims.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- **Verification command**: `python engineering/scripts/test_ticket_08_product_entity.py` -> 4 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/product_entity_resolver.py`, `engineering/scripts/test_ticket_08_product_entity.py`.
- **Adversarial check**: Hardware revision with changed interfaces cannot inherit obsolete claims (100% precision).
- **Limitations**: None. 4-level identity resolution operational.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
