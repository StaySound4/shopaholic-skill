# 08 — Resolve Canonical Product, Region SKU, Revision, and Batch

**What to build:** Create the product-identity hierarchy (`Canonical Product -> Region SKU -> Revision -> Batch`), link Region SKUs to jurisdiction-specific compliance identifiers (China 3C/CEL, US FCC ID/UL, EU CE/EPREL, Japan PSE), and ensure claim scope follows the narrowest evidence-supported identity.

**Blocked by:** 05

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Bundle/accessory SKUs can map to one canonical host product.
- [ ] Region variants remain distinct when decision-relevant properties (voltage 110V/220V, certification, warranty) differ.
- [ ] Region SKUs record jurisdiction compliance identifiers (3C, FCC ID, EPREL, UL, PSE) and structured certifications.
- [ ] Revision and batch can be represented independently.
- [ ] Batch recommendation provides launch window and physical SN/nameplate verification method.
- [ ] Unknown lower-level identity is not guessed.

## Verification procedure

Pass: same main-unit GTIN in different bundles resolves one canonical product; CN (3C/220V) and US (FCC/UL/120V) variants remain distinct. Adversarial: a revision with changed interface cannot inherit old-revision feature claims.

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
