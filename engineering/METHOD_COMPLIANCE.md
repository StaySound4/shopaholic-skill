# Method Compliance — Uploaded `to-spec` and `to-tickets`

The user-supplied method skills are copied under `method-snapshot/` and hash-recorded.

## `to-spec` compliance

- Testing seams were selected before writing the spec and are documented in `TEST_SEAMS.md`.
- The spec uses the required sections, in order:
  - Problem Statement
  - Solution
  - User Stories
  - Implementation Decisions
  - Testing Decisions
  - Out of Scope
  - Further Notes
- User stories are intentionally extensive and cover happy paths, negative paths, ambiguity, source failure, region/version/batch, used goods, international data, safety, pricing, corrections, maintenance and evaluation.
- Implementation decisions describe behavior/data flow/state rather than prescribing implementation file paths or code snippets.
- Testing decisions are realistically executable: controlled/frozen/live tiers, paired conditions, real raw outputs, controls, blind review, replicates, statistical analysis and release gates.

## `to-tickets` compliance

- Tickets are tracer-bullet slices wherever possible: each creates an observable behavior and verification path.
- Prefactor tickets are limited to the minimum measurement seam and immutable experiment contracts needed to make later work testable.
- Wide migration follows expand/migrate/contract: introduce structured semantics, migrate behaviors/tests, then contract legacy quotas/taxonomies.
- Every ticket has:
  - title;
  - `What to build`;
  - explicit blockers;
  - `Status: ready-for-agent`;
  - acceptance criteria;
  - fresh-context verification procedure;
  - evidence-to-attach requirements;
  - stop conditions.
- Local ticket mirrors are also emitted under `.scratch/shopaholic-v1/issues/`, matching the method skill’s local-tracker fallback convention.
