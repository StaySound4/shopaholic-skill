# AI Execution Runbook — One Run at a Time

This runbook is intentionally repetitive. A low-capability agent should follow it literally.

## Before touching implementation

1. Read `SPEC.md` once.
2. Read the ticket you were assigned.
3. Read only that ticket’s blockers. If any blocker is not complete, STOP.
4. Read the acceptance criteria.
5. Create a scratch note with one checkbox per criterion.
6. Do not solve later tickets “while you are here”.

## Before running an experiment

1. Locate the experiment manifest.
2. Confirm `preregistered=true`.
3. Confirm case-set hash matches the actual case file.
4. Confirm condition list contains the condition you are about to run.
5. Confirm the run row gives you case, condition, replicate, and run ID.
6. If any item does not match, STOP with `INVALID_PROTOCOL`.

## Running a single case

1. Start fresh context.
2. Load only the required condition.
3. Copy the user prompt exactly.
4. For Tier D/F, provide exactly the evidence packet. Do not add outside facts unless allowed.
5. Do not coach the model.
6. When it finishes, copy raw output verbatim to the run artifact.
7. Save tool/source trace if present.
8. Save structured Decision Record if present.
9. Fill run metadata.
10. Validate schema.
11. Do not judge quality yet.

## Automated scoring

1. Run deterministic schema/fixture checks first.
2. If the run cannot be parsed because the implementation failed to produce required structure, record the product failure; do not hand-repair JSON.
3. Run case assertions.
4. Store per-assertion pass/fail with reason.
5. Never set a condition-level score manually.

## Human review packet

For a human-review case:

1. Generate an anonymized packet without condition name.
2. Include the case evidence packet/gold facts allowed for judging.
3. Randomize answer order for pairwise review.
4. Ask the reviewer to use the scoring rubric.
5. Store reviewer ID/pseudonym and independent annotations.
6. Do not show reviewer 2 reviewer 1’s answer.
7. Adjudicate only after both have submitted.

## When a source fails

- If Tier D/F source content is missing from the case packet: `INVALID_PROTOCOL`.
- If Tier L authoritative source is unavailable: `BLOCKED_SOURCE`.
- Do not replace it with a weaker source and pretend nothing changed.

## When an implementation fails

- Wrong recommendation/constraint/evidence behavior: `FAIL_PRODUCT`.
- Tool/runtime cannot perform declared capability: `BLOCKED_CAPABILITY`.
- Scorer has a bug or control fails: `FAIL_EVALUATOR` / invalidate experiment as required.

## After all runs

1. Count complete, failed, blocked, invalid separately.
2. Verify controls before target interpretation.
3. Aggregate paired metrics.
4. Produce confidence intervals/tests.
5. Compare to preregistered gates.
6. Write limitations.
7. Only then write a conclusion.

## Forbidden shortcuts

- No hard-coded “oracle” outcome table.
- No editing model outputs before scoring.
- No changing expected answers after seeing target output under the same case version.
- No deleting failed runs.
- No using a model judge as the sole factual authority on live web.
- No calling three complaints a statistically measured defect rate without denominator evidence.
- No converting a blocked source into a pass.
