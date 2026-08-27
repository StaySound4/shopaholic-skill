# 15 — Make Round 1 adaptive and cap the conversation at three rounds

**What to build:** Implement intake that performs broad prior catalog and scientific principle search (+30%~50% price headroom without premature truncation), ingesting category-specific physics, asking only unresolved variables that change the decision, and permitting direct delivery when the request is already sufficient.

**Blocked by:** 04, 11, 14

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Round 1 performs broad prior catalog search (+30%~50% price headroom and higher-tier flagship architecture exploration) before questioning.
- [ ] User-declared hard constraints (e.g. 2000 budget) do NOT prematurely truncate broad search exploration of engineering physics and failure modes.
- [ ] Round 1 questions strictly focus on engineering context, physical constraints, and core pain points informed by the broad search.
- [ ] Purchase market scope (domestic vs overseas) and report layout questions are NOT asked in Round 1.
- [ ] Already supplied values are not re-asked.
- [ ] At most two clarification rounds precede final delivery.

## Verification procedure

Pass: fully specified case goes directly to research/final; broad search on 2000-budget case explores 3000 flagship tech to ground Round 1 questions without recommending over-budget picks. Adversarial: “推荐个咖啡机” asks 2-3 use-relevant questions, not output-view choices.

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
