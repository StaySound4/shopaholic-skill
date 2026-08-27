# 30 — Add explicit degraded modes for source/tool unavailability

**What to build:** Define explicit degraded modes (`partial`, `blocked`, `live-source-unavailable`) when essential web search tools or regulatory databases are inaccessible, strictly prohibiting memory hallucinations.

**Blocked by:** 11, 22, 23

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Unavailability of a required web search tool or authoritative database produces explicit runtime degraded state (`decision_status: "source_unavailable" | "blocked"` and evaluation failure code `BLOCKED_SOURCE`), not silent fallback to ungrounded memory.
- [ ] Partial evidence produces bounded recommendation with explicit lower confidence (`B` or `U`) and `decision_status: "partial"`.
- [ ] Blocked conclusions explicitly identify the missing source and allow clean re-run.
- [ ] The system never pretends a live verification succeeded when tools were offline.
## Verification procedure

Pass: unavailable mandatory certification database blocks verification. Adversarial: weaker blog cannot automatically replace regulator and retain S grade.

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
