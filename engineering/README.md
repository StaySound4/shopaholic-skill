# Shopaholic v1 Engineering Pack

This pack is the revised **to-spec -> to-tickets** output for the uploaded Shopaholic skill snapshot.

It is intentionally designed for low-capability implementation agents: every ticket is bounded, explicitly blocked, independently verifiable, and requires evidence artifacts before completion.

## What is inside

- `SPEC.md` — behavioral product/engineering specification. No implementation file-path prescriptions in the spec body.
- `TEST_SEAMS.md` — the minimal stable testing seams chosen before decomposition.
- `CURRENT_STATE_AUDIT.md` — problems observed in the uploaded snapshot and why they matter.
- `ARCHITECTURE_DECISIONS.md` — durable decision log so later agents do not reintroduce rejected designs.
- `SOURCE_REGISTRY.md` — source families, what each may prove, and what it may not prove.
- `TRACEABILITY_MATRIX.md` — maps each spec requirement to tickets and tests.
- `TICKET_INDEX.md` — ordered execution plan.
- `tickets/` — one atomic ticket per file, each with acceptance criteria, verification, evidence, and stop conditions.
- `schemas/` — machine-readable contracts for product identity, claims, sources, decisions, evaluation cases, run records, and experiment manifests.
- `evals/` — real experiment protocol, scoring rubric, seed cases, runbook, and report template.
- `scripts/` — deterministic validators/randomizers/scorers for experiment bookkeeping.
- `current-skill-snapshot/` — exact uploaded Shopaholic skill used as the baseline snapshot.
- `SNAPSHOT_MANIFEST.json` — hashes for the baseline snapshot.

## Mandatory execution order

1. Read `SPEC.md`.
2. Read `TEST_SEAMS.md`.
3. Read `TICKET_INDEX.md`.
4. Work on **one ready ticket only**.
5. Run the ticket verification procedure in a fresh context.
6. Save the required evidence artifact(s).
7. Mark a ticket complete only when all acceptance criteria have evidence.
8. Do not start tickets whose blockers are incomplete.
9. Do not claim an improvement until the paired experiment and release-gate tickets pass.

## Non-negotiable research rule

A benchmark is not an experiment merely because it prints numbers. Any score used to claim improvement must be computed from actual model outputs or independently annotated records. Hard-coded expected scores, manually assigned PASS/FAIL values, or examples written after seeing the answer are demonstrations only and must never be presented as empirical validation.
