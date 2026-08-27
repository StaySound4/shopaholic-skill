# 23 — Record commercial relationships, sample provenance, and source conflicts

**What to build:** Attach brand/seller/affiliate/sponsorship/loaner/unknown metadata and sample provenance to evidence, and use them as claim-specific bias context.

**Blocked by:** 05, 06, 22

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Relationships are recorded when known.
- [ ] Sponsored/brand source is not automatically discarded for its own declared spec.
- [ ] It cannot alone establish independent superiority.
- [ ] Conflicts across sources remain explicit.

## Verification procedure

Pass: manufacturer-supplied review still supports observed measurement with disclosed caveat if method transparent; ad copy cannot support comparative durability. Adversarial: “affiliate” flag alone must not erase an independently reproducible measured fact.

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
