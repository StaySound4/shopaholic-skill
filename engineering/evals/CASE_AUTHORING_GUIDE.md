# Evaluation Case Authoring Guide

## Goal

Write cases that can falsify a behavior. A case is not useful if almost any plausible answer can be marked correct.

## Step 1 — Choose exactly one primary failure mode

Examples:
- user hard constraint leakage;
- region SKU conflation;
- unsupported OEM inference;
- anecdote -> prevalence overclaim;
- historical-price label misuse;
- unnecessary second-round question.

Secondary assertions are allowed, but the primary failure mode must be explicit.

## Step 2 — Choose tier

### D controlled evidence
Use when the behavior can be tested with an artificial but fully explicit world. This is preferred for logic regressions.

Rules:
- evidence packet is complete for the case;
- outside factual knowledge is irrelevant or forbidden;
- gold assertions must be deterministic where possible.

### F frozen real evidence
Use when source interpretation itself matters.

Rules:
- capture real source content before target runs;
- save retrieval date, locator, and content hash;
- human gold is prepared from the frozen packet before target outputs are viewed;
- source must not be silently refreshed inside the same experiment version.

### L live web
Use when freshness/tool behavior is the target.

Rules:
- do not hard-code facts likely to change;
- assertions focus on process, source-role discipline, exact scoping, and current evidence capture;
- save the full tool/source trace;
- analyze live cases separately.

## Step 3 — Write gold assertions before target output

Good:
- `must_not_recommend: B`
- `claim_status: unverified`
- `research_budget: R0`
- `must_not_call: historical_range`
- `must_keep_roles_separate: true`

Bad:
- “answer should be good”
- “should mention enough sources”
- “should probably recommend A”

## Step 4 — Add a trap/adversarial branch

Every important behavior should have both:
- a positive case where it should trigger;
- a negative case where it should not.

Examples:
- exact recall batch excludes / unrelated revision does not;
- FCC Change in ID supports same-design / visual similarity alone does not;
- close ranking triggers sensitivity / dominated candidate does not;
- vague request asks questions / fully specified request skips questions.

## Step 5 — Avoid evaluator leakage

Do not:
- include target-system vocabulary in the prompt unless a real user would use it;
- write the case after seeing a target failure and keep the same case-set version;
- let the same model that generated the answer invent the factual gold from live web without independent evidence.

## Step 6 — Version honestly

Any change to prompt, evidence packet, or gold assertion increments case version and changes the case-set hash. Published results continue to point to the old version.

## Minimum acceptance for a beta case

- stable ID/version;
- declared tier/category;
- exact prompt;
- evidence packet when D/F;
- at least one falsifiable assertion;
- whether human review is required;
- primary failure mode noted;
- reviewed before target run.
