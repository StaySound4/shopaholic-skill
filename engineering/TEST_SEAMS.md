# Testing Seams

The decomposition deliberately minimizes test seams. Tests should be placed at the highest stable external behavior that can fail meaningfully.

## Seam 1 — End-to-End Decision Behavior

**Question:** Given a shopping request and available evidence, does Shopaholic produce a decision that respects hard constraints, accurately communicates uncertainty, uses the allowed purchase market, and gives a useful recommendation?

This seam covers:
- conversation state transitions
- hard/user/preference constraints
- research-budget selection
- output scope
- candidate selection
- correction behavior
- used-goods behavior
- concise final answer

Primary measurement:
- exact hard-constraint violation rate
- usefulness pairwise preference
- question burden
- candidate precision
- abstention correctness

Do **not** create one unit test per prompt sentence unless the behavior cannot be observed at this seam.

## Seam 2 — Product Identity + Claim/Evidence Ledger

**Question:** Can the system correctly resolve the product/region/revision/batch and attach every high-impact claim to evidence that is suitable for that claim?

This seam covers:
- canonical product identity
- region SKU
- revision/batch
- brand owner / applicant / manufacturer / factory / ODM/OEM / importer / seller
- origin semantics
- release/certification dates
- claim status and scope
- source conflicts and commercial relationships
- recall scope

Primary measurement:
- entity resolution accuracy
- provenance-role accuracy
- high-impact claim support rate
- source-role appropriateness
- unsupported-claim rate
- disputed-evidence handling

## Seam 3 — Deterministic Calculations

**Question:** Do computations produce the same correct answer independent of language-model reasoning?

Use deterministic code for:
- currency/landed-cost arithmetic when sufficient inputs exist
- weight normalization
- Pareto dominance checks
- sensitivity flip-point calculation
- experiment randomization
- metric aggregation
- confidence intervals/statistical tests

Primary measurement:
- exact fixture pass rate (target 100%)

## Seam 4 — Release Gate

**Question:** Does a frozen, predeclared experiment show that the target version improves or preserves critical metrics relative to the uploaded baseline without evaluator artifacts?

This seam covers:
- baseline vs full-skill paired runs
- ablations
- positive and sham controls
- blinded annotation
- repeated stochastic trials
- paired statistical analysis
- immutable manifests
- cross-runtime regressions

Primary measurement:
- preregistered gates only
- confidence intervals and paired tests
- control validity

## Why these seams

They let a weak implementation agent progress safely:
1. build/verify one structural layer at a time;
2. avoid brittle tests for every wording rule;
3. preserve observability of real user outcomes;
4. prevent fake confidence from self-authored expected scores.
