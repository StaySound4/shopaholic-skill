# 02 — Define machine-readable evaluation cases and immutable manifests

**What to build:** Introduce versioned case and experiment contracts so a weak agent cannot change prompts, assertions, gates, or conditions after seeing target outputs without creating a new experiment version.

**Blocked by:** 01

**Status:** completed

## Acceptance criteria

- [x] Every case has stable ID/version/tier/prompt/assertions.
- [x] Experiment manifest stores case-set hash, conditions, replicates, seed, model/runtime and release gates.
- [x] Changing a case changes the case-set hash.
- [x] A preregistered manifest cannot be mutated without a new experiment ID.

## Verification procedure

Validate at least 40 seed cases; mutate one prompt byte and show case-set hash changes. Adversarial: attempt to reuse a preregistered manifest with the changed case set and require INVALID_PROTOCOL.

Always execute verification in a fresh context. Save the exact prompt/input, raw output, structured record if available, tool/source trace, and pass/fail rationale. Include at least one expected-pass path and the adversarial path above. Do not repair a failed output before scoring.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- **Verification command**: `python engineering/scripts/test_ticket_02_manifests.py` -> 4 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/manifest_tool.py`, `engineering/scripts/test_ticket_02_manifests.py`.
- **Adversarial check**: Mutated case set evaluated against preregistered manifest triggers `INVALID_PROTOCOL` with 100% precision.
- **Limitations**: None. Immutable manifest contracts enforced.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
