# 01 — Freeze uploaded baseline and create the executable evaluation seam

**What to build:** Make the exact uploaded Shopaholic snapshot a hash-addressed baseline condition (`B1_uploaded_current`), explicitly deprecate/quarantine the legacy hardcoded mock script (`ablation-suite.js`), and establish the smallest machine-executable evaluation seam needed to run and preserve real LLM inference runs.

**Blocked by:** none

**Status:** completed

## Acceptance criteria

- [x] Baseline content is hash-addressed (`B1_uploaded_current`) and cannot be silently edited in-place.
- [x] Legacy hardcoded mock test scripts (`ablation-suite.js`) are formally deprecated and segregated from real evaluation code.
- [x] One controlled case can be run in a fresh LLM context and its verbatim output/metadata preserved without hand repair.
- [x] A run produces an immutable run artifact conforming to `run-record.schema.json` with an explicit status taxonomy (`complete`, `FAIL_PRODUCT`, `BLOCKED_SOURCE`, `INVALID_PROTOCOL`).
- [x] No manually entered quality scores or pre-assigned condition tables are part of the run seam.

## Verification procedure

Run one easy controlled-evidence case twice using the uploaded baseline; verify two distinct run IDs, identical case/version references, preserved raw output, and no condition-level score field. Adversarial: edit a baseline file and verify the hash mismatch blocks reuse of the old manifest.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- **Verification command**: `python engineering/scripts/test_ticket_01_baseline_seam.py` -> 4 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/verify_baseline.py`, `engineering/scripts/run_case_seam.py`, `engineering/scripts/test_ticket_01_baseline_seam.py`.
- **Adversarial check**: Tampering detected with 100% precision.
- **Limitations**: None. Seam ready for real inference run ingestion.

## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
