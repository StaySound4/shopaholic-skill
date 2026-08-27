# 33 — Add freshness guards for static references and runtime temporal facts

**What to build:** Prevent stale standards, obsolete regulatory statuses (e.g. labeling active standards like GB 4706.1-2024 as "upcoming"), wrong standard code citations (e.g. confusing IEEE 1789 flicker mitigation with IEEE 1788 RF immunity), and expired model/pricing facts from being presented as current by enforcing live verification anchors and expiry rules.

**Blocked by:** 10, 22, 27

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Fixed year literals (2025/2026) in search queries are dynamically replaced with runtime year derivation.
- [ ] Regulatory standard statuses (`active`, `upcoming`, `superseded`, `repealed`) are verified live against authoritative standard databases (`std.samr.gov.cn`, IEEE SA, IEC, FDA).
- [ ] Known standard code errata are enforced (LED flicker is IEEE 1789-2015, not IEEE 1788; appliance safety is mandatory GB 4706.1-2024 active 2026-08-01).
- [ ] Expired/stale reference content triggers live reverification or lowers evidence confidence to `U`/`B`.
- [ ] Stable physical principles (optics, thermodynamics, acoustics) remain undated where appropriate.

## Verification procedure

Pass: runtime year changes dynamically; obsolete "upcoming" phrasing for active standards (GB 4706.1-2024) is detected and corrected; IEEE 1789 vs 1788 is accurately resolved. Adversarial: a stale reference text cannot override a live query from `std.samr.gov.cn`.

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
