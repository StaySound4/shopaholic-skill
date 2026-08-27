# Engineering Pack Self-Test Log

Date: 2026-08-27

These tests validate the **planning/evaluation pack itself**. They are not evidence that Shopaholic v1 improves shopping quality; that requires Tickets 34–40.

## 1. Bundle structural validator

Initial result: **FAIL**.

Reason: the validator’s anti-fake-benchmark static rule matched the validator source itself because its own implementation contained the inspected keyword pattern.

Action: exclude the validator itself from that content scan.

Rerun result:

`PASS — 48 seed cases, 40 tickets`

Why this is retained in the log: validators must be allowed to fail, including on their own implementation mistakes. A validator that always reports PASS is not useful.

## 2. JSON Schema validation

Validated all 48 seed cases against the evaluation-case schema and the example experiment manifest against the experiment-manifest schema.

Result: **PASS — 48/48 cases**.

## 3. Deterministic sensitivity fixture

Input:
- candidate A criteria: 90,60
- candidate B criteria: 70,90
- criterion-1 current weight: 0.3

Expected flip weight: `0.4`.

Observed: `0.4`.

Result: **PASS**.

## 4. Experiment-plan randomization reproducibility

Generated two plans with identical case file, condition list, replicate count and seed `123`.

Byte comparison result: **identical**.

Result: **PASS**.

## 5. Real-row metric aggregation fixture

Supplied four actual per-run rows (two cases x baseline/target) to the scorer. The scorer computed baseline/target means, paired difference, bootstrap confidence interval and sign-test value from the rows.

Expected paired difference on the test metric: `0.5`.

Observed: `0.5`.

Result: **PASS**.

Important: no condition score exists inside the scorer source.

## 6. Preregistration guard

Attempted release-gate evaluation using the example manifest while `preregistered=false`.

Expected: refuse confirmatory gate evaluation.

Observed: refused.

Result: **PASS**.

## 7. Release-gate mutation test

With a preregistered temporary manifest:

- all metrics satisfying thresholds -> overall `PASS`;
- mutate `fabricated_source_rate` from `0.0` to `0.01` against a max gate of `0.0` -> overall `FAIL`.

Result: **PASS**.

## 8. Self-test aggregate

The bundled self-test reports:

`SELFTEST PASS: validator, sensitivity, randomization, derived scoring, preregistration guard, and release-gate mutation all behave as expected.`

Again: this validates experiment plumbing, not the future product outcome.
