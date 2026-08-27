# 27 — Modularize category knowledge as live-verification playbooks

**What to build:** Split monolithic category knowledge into selectively loadable modular **Wayfinding Playbooks (指路导航剧本)** (`references/categories/<category-slug>.md` with lightweight `INDEX.md` router), implementing a **3-Tier Progressive Loading Architecture** to optimize context window efficiency, eliminate attention dilution, and enforce strict single-category context isolation.

**Blocked by:** 06, 11, 22

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Category knowledge is split into standalone modular files (`references/categories/*.md`) with an index router (`INDEX.md`).
- [ ] 3-Tier progressive loading is strictly enforced: Tier 1 Core Router (`SKILL.md`, <150 lines), Tier 2 Category Playbook (on-demand single file), Tier 3 Deep Forensics (on-demand R2/R3).
- [ ] Context isolation is absolute: loading Category A (e.g. coffee) strictly excludes all other category files from the context window.
- [ ] Stable decision physics (underlying trade-offs, measurement methods, failure hypotheses) and volatile market facts are strictly decoupled.
- [ ] Dual-market wayfinding search anchors are embedded per category (pointing to GB/CCC portals vs UL/CE/TÜV/VESA/OEKO-TEX/ECE registries).
- [ ] No hoarding of static standard texts, temporary clauses, or volatile model lists; all volatile facts rely on live search routing.
- [ ] No universal BOM teardown requirement is imposed across divergent categories.
- [ ] Long-tail geek categories (HiFi DAC/amps, 3D printing/resin, road bike groupsets, alpine gear) follow the standard playbook structure.

## Verification procedure

Pass: coffee query loads only `01-coffee.md` and tests ingredients/compliance rather than BOM teardown; HiFi query loads `hifi-audio.md` and tests SINAD/THD+N rather than consumer review stars. Adversarial: an obsolete standard status or hardcoded product price cannot remain normative without date/reverification anchors.
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
