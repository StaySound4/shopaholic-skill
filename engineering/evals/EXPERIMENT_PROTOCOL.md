# Shopaholic Real Experiment Protocol v1

## 0. What this protocol is for

This protocol exists to answer one question:

> Does the target Shopaholic behavior improve shopping-decision correctness/usefulness relative to the uploaded baseline, and which features cause the change?

If the procedure below is not followed, do not describe the result as an experiment proving improvement.

## 1. Experimental conditions

Required:

- `B0_no_skill` — same model/runtime, no Shopaholic skill.
- `B1_uploaded_current` — exact uploaded Shopaholic snapshot whose hashes are in the bundle manifest.
- `T_full` — target implementation.

Feature ablations:

- `A_no_claim_ledger`
- `A_no_provenance`
- `A_no_research_budget`
- `A_no_risk_adjudication`
- `A_no_market_scope_split`
- `A_no_sensitivity`

Evaluator controls:

- `C_positive_bad_evidence` — deliberately allow unsupported/role-mismatched evidence so the evaluator must catch the degradation.
- `C_sham_style` — improve formatting/verbosity only, without decision-logic changes; correctness/evidence scores should not materially improve.

## 2. Evidence tiers

### Tier D — Controlled evidence

Use synthetic-but-explicit evidence packets. These cases test logic without web drift. Facts inside the case are the entire allowed world for that run. If the model invents information outside the packet, score it as unsupported.

### Tier F — Frozen real evidence

Use real retrieved source content saved with retrieval date and content hash. Reviewers score only against the frozen packet. Re-fetching is not allowed inside the same published experiment version.

### Tier L — Live web

Use current live sources. Save every source/tool trace. Tier L is analyzed separately. A live-source outage is `BLOCKED_SOURCE`, not a silent substitution.

## 3. Dataset sizes

Milestones:

- smoke: 40 D cases;
- beta: >=100 fixed D/F cases plus >=10 L cases;
- v1.0: >=200 fixed D/F cases plus >=20 L cases.

Do not add cases after viewing target failures and then pretend they were preregistered. New/changed cases increment the case-set version/hash.

## 4. Required case strata

At minimum:

1. safety/compatibility hard constraints;
2. user hard constraints;
3. soft preference ranking;
4. China-only / overseas-only / both scopes;
5. region SKU mismatch;
6. revision/batch distinction;
7. corporate/provenance-role separation;
8. OEM same-platform positive and false-positive negative cases;
9. origin inference traps;
10. time/date semantic traps;
11. source-role mismatch;
12. source conflict/disputed claim;
13. insufficient evidence/abstention;
14. exact recall scope and unrelated recall scope;
15. anecdotal failure signal without denominator;
16. R0/R1/R2/R3 research-budget behavior;
17. used-market eligible and discouraged categories;
18. current price vs historical price semantics;
19. cross-border landed cost;
20. prompt injection embedded in retrieved evidence;
21. unavailable authoritative source;
22. correction behavior;
23. close ranking with sensitivity flip;
24. dominant ranking where sensitivity must not run;
25. pivot-cost relevant and irrelevant cases.

## 5. Preregistration

Before running `T_full`:

1. freeze the case set;
2. compute/store case-set hash;
3. freeze scoring rubric version;
4. choose conditions;
5. choose replicate count;
6. choose model/runtime versions;
7. choose randomization seed;
8. store release gates;
9. create an experiment manifest;
10. mark `preregistered=true`.

After preregistration, changing a gate/case/condition requires a new experiment ID.

## 6. Run procedure — exact steps for a low-capability agent

For every row in the randomized run plan:

1. Create a new empty run directory named by `run_id`.
2. Start a **fresh conversation/context**. Do not reuse prior case messages.
3. Load exactly the condition declared in the row. Do not mix instructions from other conditions.
4. Present the case prompt exactly. For Tier D/F, provide the declared evidence packet and prohibit external facts unless the case says otherwise.
5. Let the model finish. Do not manually fix, continue, paraphrase, or “help” it unless the case explicitly includes a scripted user second turn.
6. Save every assistant message verbatim to `raw_output`.
7. Save tool calls/source locators if the runtime exposes them.
8. Save the structured Decision Record if the condition supports it.
9. Record model, runtime, skill hash, tools, start/end time, token/search count when available.
10. Validate the run record schema.
11. If the model/tool failed, choose exactly one status:
   - `FAIL_PRODUCT`
   - `FAIL_EVALUATOR`
   - `BLOCKED_CAPABILITY`
   - `BLOCKED_SOURCE`
   - `INVALID_PROTOCOL`
12. Never delete a bad run. A retry receives a new run ID/replicate record.

## 7. Replication and ordering

- Tier D deterministic fixtures may use one replicate if the runtime is guaranteed deterministic; otherwise use >=3.
- Tier F and L use >=3 replicates for stochastic models.
- Randomize condition order within each case using the stored seed.
- Do not run all baseline conditions first and all target conditions later when model/service drift is possible.
- When rate limits require batching, interleave conditions as much as possible and record batch/time.

## 8. Automated scoring

Automate only outcomes with explicit machine-checkable ground truth:

- hard-constraint compliance;
- forbidden market/used inclusion;
- exact product/region/revision/batch identity;
- expected `verified/disputed/unverified/blocked` state;
- research budget;
- current-vs-historical price label;
- question/round count;
- deterministic landed-cost fixture;
- deterministic Pareto/sensitivity fixture;
- explicit source-role assertions when the structured ledger is present.

The scorer reads run artifacts. It must never contain a manually typed condition score such as “T_full=100”.

## 9. Human scoring

### Factual/evidence/safety holdout

- Two independent reviewers per designated case.
- Reviewers receive: case ID, evidence packet, anonymized answer A/B or single anonymized answer.
- Reviewers do not receive the condition label.
- Disagreements are adjudicated by a third reviewer or documented consensus step.
- Report agreement statistic where possible.

### Usefulness preference

- Blind pairwise comparison of `T_full` vs `B1_uploaded_current`.
- Randomize left/right placement.
- Options: A better / tie / B better.
- Reviewer must also flag any correctness/safety defect; a prettier wrong answer cannot win usefulness.

## 10. Evaluator controls

Before interpreting target results:

### Positive control

`C_positive_bad_evidence` must show a materially worse unsupported-claim/source-role score than a valid condition. If not, the evaluator is too weak.

### Sham control

`C_sham_style` should not receive a material improvement on evidence/correctness metrics merely from formatting. If it does, human/scoring rubrics are presentation-biased.

### Deterministic mutation test

Inject at least one known wrong sensitivity/price calculation into a test fixture. The deterministic scorer must fail it.

If any control fails: mark experiment `INVALID_PROTOCOL` until the evaluator is repaired and the experiment rerun.

## 11. Statistical analysis

All confirmatory comparisons are paired by case.

Report:

- baseline and target metric value;
- paired difference;
- 95% confidence interval;
- applicable paired test;
- sample size and blocked/invalid counts.

Recommended:

- paired binary outcomes: McNemar-style test and/or paired bootstrap CI;
- ordinal/continuous paired scores: Wilcoxon signed-rank where appropriate + paired bootstrap CI;
- pairwise preference: win/tie/loss plus bootstrap/binomial-style CI on non-ties;
- multiple confirmatory ablations: Holm correction.

P-values never replace effect sizes/CI.

## 12. Release gates

Frozen before experiment execution:

- fabricated citations/sources: 0 on adjudicated D/F cases;
- safety/compatibility hard-constraint violations: 0;
- user hard-constraint compliance >=99%;
- applicable product+region/revision identity accuracy >=95%;
- high-impact source-role appropriateness >=95%;
- evidence-insufficiency handling >=95%;
- deterministic math fixtures =100%;
- research-budget compliance >=95%;
- no case needs more than two clarification rounds before final delivery;
- sufficient-input fixed cases must not add gratuitous Round 2;
- no critical metric shows a practically meaningful regression vs uploaded baseline;
- blind usefulness target: T_full wins >=60% of non-tie comparisons, with reported CI;
- all controls pass.

If a gate fails, release may still continue only as an explicitly documented experimental/pre-release build; do not claim the gate passed.

## 13. Ablation interpretation

Each ablation has a preregistered primary outcome:

- no claim ledger -> unsupported/source-role/conflict handling;
- no provenance -> identity/provenance/OEM/origin accuracy;
- no research budget -> search cost/question burden/low-vs-high risk behavior;
- no risk adjudication -> anecdote/recall scope behavior;
- no market-scope split -> overseas leakage/domestic-only compliance;
- no sensitivity -> flip-point/helpfulness on close-decision cases.

Do not call an ablation “important” merely because an unrelated global score changes.

## 14. Experiment conclusion language

Allowed:

> “On experiment EXP-..., using N fixed cases and K replicates, T_full reduced hard-constraint violations from X to Y and improved blind usefulness preference by Z points; 95% CI ...”

Not allowed:

> “The ablation suite proves the mechanism is indispensable”

when results were hard-coded, cases were changed post hoc, controls failed, or raw outputs are unavailable.
