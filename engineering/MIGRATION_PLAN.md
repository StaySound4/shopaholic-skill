# Migration Plan — Expand / Migrate / Contract

## Phase 0 — Measurement before redesign

Tickets 01–03.

Purpose: freeze the current skill, create immutable run/case contracts, and validate the evaluator with controls. Do not change shopping behavior yet. Without this phase, later “improvements” cannot be attributed or regression-tested.

Exit evidence:
- baseline hashes;
- at least one preserved real baseline run;
- case-set/manifest validation;
- evaluator controls designed and capable of failing.

## Phase 1 — Expand new decision semantics alongside legacy behavior

Tickets 04–14.

Introduce:
- three constraint classes;
- claim/evidence ledger;
- evidence roles and S/A/B/U;
- product/region/revision/batch identity;
- provenance graph;
- origin/date semantics;
- research budget;
- dynamic discovery stop;
- risk adjudication;
- market-scope split.

Legacy output may still exist during this phase. New structured records must be observable and testable.

## Phase 2 — Migrate interaction and recommendation paths

Tickets 15–20.

Move the user-facing flow to:
- adaptive Round 1;
- optional search-informed Round 2;
- category-aware used market;
- strict price semantics;
- landed-cost handling;
- concise decision-first output.

Exit evidence: end-to-end fixed cases pass without relying on legacy quotas/taxonomy.

## Phase 3 — Contract obsolete behavior

Ticket 21.

Only now remove:
- L1/L2/L3/L4 universal hierarchy;
- fixed source quotas;
- fixed candidate quotas;
- A mature / B blackhorse labeling collision;
- fixed temporal year rules.

This phase must include static audit plus regression cases so the project does not accidentally keep both contradictory systems.

## Phase 4 — Deep evidence, ranking and resilience

Tickets 22–30.

Add:
- authoritative domestic/global routing;
- interest/conflict metadata;
- Pareto-first ranking;
- deterministic sensitivity;
- conditional pivot cost;
- modular category playbooks;
- truth-first corrections;
- retrieved-content security;
- degraded modes.

## Phase 5 — Real evaluation system and release discipline

Tickets 31–36.

Automate objective scoring, blind human review, execute paired experiments, compute statistics, and enforce preregistered gates.

No public “measured improvement” claim before this phase completes.

## Phase 6 — Packaging, governance, compatibility, evidence dossier

Tickets 37–40.

Validate distribution, community contribution governance, cross-runtime regression, and publish a traceable experiment dossier.
