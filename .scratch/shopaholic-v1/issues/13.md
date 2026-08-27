# 13 — Replace incident-count rules with scoped safety-signal adjudication

**What to build:** Abolish mechanical pseudo-statistical thresholds ("1 incident = veto", ">=3 complaints = common defect"), replace them with a 7-stage risk adjudication state machine (`discovered -> authenticity -> deduplication -> scope/batch -> causal & misuse check -> regulatory action -> decision impact`), enforce denominator exposure awareness (differentiating 3/500 from 3/5,000,000), and reserve hard exclusion for sufficiently verified, scoped safety/recall evidence.

**Blocked by:** 06, 08, 10

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Mechanical "1 incident veto" and "3 complaints common defect" rules are completely eradicated.
- [ ] An isolated severe incident is classified as a `risk_signal` that triggers escalated investigation rather than instant product veto.
- [ ] Hard exclusion requires an official scoped recall (SAMR/CPSC/EU Safety Gate), confirmed causal defect, or verified failure evidence.
- [ ] Plausible user misuse, non-OEM accessory usage, and unverified anecdotal forum claims are evaluated and not conflated with intrinsic manufacturing defects.
- [ ] Complaint volume is evaluated strictly in relation to exposure denominator; numeric failure rates without sales exposure are prohibited.
- [ ] Cross-platform duplicate complaints from the same user are deduplicated into a single incident.
- [ ] Defects in early batches or retired revisions (Rev A) are isolated and do not automatically exclude fixed revisions (Rev B/C).
- [ ] Unverified risk signals and bounded uncertainties are disclosed transparently in the decision record without arbitrary candidate elimination.

## Verification procedure

Pass: exact recall batch hard-excludes; 3 complaints on a 5-million-unit product are treated as a watch point rather than a confirmed common defect; unverified single forum anecdote triggers investigation without instant veto. Adversarial: one unverifiable forum fire cannot cause product-wide veto or numeric defect-rate claim.
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
