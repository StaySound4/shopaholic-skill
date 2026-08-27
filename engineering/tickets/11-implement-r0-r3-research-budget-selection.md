# 11 — Implement R0-R3 research-budget selection

**What to build:** Choose research depth and candidate discovery scope from safety/regulatory stakes, price/irreversibility, complexity, evidence scarcity, installation risk, and ownership consequences, scaling from R0 (2-4 candidates for trivial purchases like 69-yuan chargers with zero BOM teardown quotas) up to R3 (safety-critical regulatory verification).

**Blocked by:** 01, 04, 05

**Status:** ready-for-agent

## Acceptance criteria

- [ ] R0-R3 selection is observable with explicit justification in the Decision Record.
- [ ] R0 (low-cost, mature standard, reversible products like cables/chargers/cases) restricts candidates to 2–4 items and forbids heavy BOM teardowns or 10+ source quotas.
- [ ] R1 handles ordinary consumer durables with standard identity and trade-off checks.
- [ ] R2/R3 handles high-value or safety-critical goods (20k appliances, medical gear) with full provenance, revision, recall, and regulatory checks.
- [ ] Research budget prevents token bloat and excessive user latency on trivial requests.

## Verification procedure

Pass: 69-yuan charger -> R0 with 2-3 candidates and fast convergence; 20k built-in appliance -> R2; regulated medical device -> R3. Adversarial: cheap safety-critical product must not become R0 solely due to price.

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
