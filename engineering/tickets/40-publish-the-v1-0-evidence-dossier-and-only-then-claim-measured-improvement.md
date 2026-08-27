# 40 — Publish the v1.0 evidence dossier and only then claim measured improvement

**What to build:** Produce a release evidence dossier linking exact skill hash, preregistered protocol, immutable case set, raw LLM run logs, scorer version, human adjudication records, paired statistical confidence intervals, and release gate decisions, with zero unverified improvement claims in README.

**Blocked by:** 35, 36, 38, 39

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Every public measured claim traces directly to an immutable experiment ID and raw run artifact.
- [ ] Unedited limitations, blocked rates, and failure rates are prominently disclosed.
- [ ] No synthetic self-test (Level 0) or mock demonstration is portrayed as experimental proof of skill effectiveness.
- [ ] Skill commit hash, case-set hash, and manifest hash are permanently stamped on the dossier.
- [ ] Public README wording strictly adheres to measured empirical scope; zero self-praise before gate clearance.
## Verification procedure

Independent reviewer follows artifact links from public claim to raw experiment summary and can reproduce aggregate metrics. Adversarial: remove raw-run linkage and require claim to be downgraded until traceability is restored.

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
