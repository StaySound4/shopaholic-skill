# 37 — Validate target Skill packaging, installer safety, and multi-runtime capability

**What to build:** Package the target skill with safe installation CLI behavior (conflict detection, timestamped backups `.bak_<timestamp>`, and diff summaries), valid metadata for supported agent environments, and honest capability declarations.

**Blocked by:** 36

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Skill installer detects existing skill directories (`.agents`, `.claude`, `.omp`, `.pi`, `.codex`) and creates timestamped backups before overwriting.
- [ ] Installer provides diff summaries and file change notices.
- [ ] Skill entrypoint and packaging validate under target runtime rules.
- [ ] Missing runtime capabilities (e.g. prompt-only vs tool-enabled) have documented fallbacks/degraded modes.
- [ ] Multi-runtime compatibility claims are restricted to verified, tested runtimes.

## Verification procedure

Pass: installer detects existing `.claude/skills/shopaholic` and creates `.bak_<timestamp>` before updating; packages validate cleanly. Adversarial: overwriting existing skill files without backup triggers failure.

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
