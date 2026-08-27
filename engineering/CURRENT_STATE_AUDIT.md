# Current State Audit — Uploaded Shopaholic Snapshot

## Scope

Audited snapshot:
- `SKILL.md`
- `references/category-checklists.md`
- `references/evidence-and-risks.md`
- `references/research-protocol.md`

This audit is about behavioral reliability, testability, and maintainability, not prose style.

## P0 — Can directly create wrong or unjustified decisions

1. **Hard-coded temporal search anchors.** Search instructions explicitly use fixed years such as 2025/2026. A skill intended to be current will age silently.
2. **Source-count quotas are treated as rigor.** Requiring 8/10 sources can reward source collection instead of claim coverage and can pressure a model to pad weak evidence.
3. **Candidate-count quotas are treated as completeness.** Requiring 10–15 discoveries and 6–10 final candidates can force low-quality additions.
4. **Universal official + independent-test requirement is category-blind.** Many product categories do not have teardown-style evidence; absence of that evidence must not encourage invention.
5. **The L1/L2/L3/L4 hierarchy conflates source class with claim validity.** A manufacturer is authoritative for its declared dimensions but not for independent durability superiority.
6. **The safety logic uses pseudo-statistical thresholds.** One severe anecdote can trigger veto and three ordinary complaints can become a “common issue” without exposure denominator, causality, duplication control, or batch scope.
7. **H/S constraint model cannot represent user-declared hard constraints.** “No used goods”, “must support HomeKit”, “budget absolutely below 3000”, and brand exclusions can be wrongly treated as mere preferences.
8. **Product identity is model-name centric.** Region SKU, revision, batch, regulatory applicant, manufacturer, factory, and OEM/ODM relationships are not first-class entities.
9. **Country/origin concepts are underspecified.** Brand country, company registration, GTIN license party, assembly country, factory location, and legal origin can be incorrectly collapsed.
10. **Release/certification/batch dates are not semantically separated.** Certification date must not silently become release date.
11. **Evidence disagreement is not a first-class state.** The system needs `verified`, `disputed`, and `unverified`, not forced convergence.
12. **Price semantics are loose.** “Current reference price” and “common range” can be presented without explicit observation date, channel, conditions, or true historical samples.
13. **Global evidence and overseas purchase are not separated.** Overseas regulatory/identity data should be usable for verification without automatically recommending overseas sellers.
14. **Static category knowledge includes time-sensitive facts and numeric heuristics.** This conflicts with the skill’s own “zero-trust/current verification” principle.
15. **Retrieved web content has no explicit prompt-injection/data-trust boundary.** Shopping pages, forums, and seller descriptions are untrusted data.

## P1 — Creates unnecessary friction or unstable behavior

16. **Three-stage interaction is mandatory in situations where one turn is already sufficient.**
17. **Round 2 forces report-format questions.** Users should not need to choose the agent’s internal representation.
18. **Used-goods question is unconditional rather than search-informed and category-aware.**
19. **The mature-vs-blackhorse A/B pool is overloaded.** It conflicts with a desired S/A/B evidence confidence scale and can force artificial symmetry.
20. **BOM “white-box” requirements are overgeneralized.** Some categories need ingredients, certification, materials, or field failure evidence instead.
21. **The anti-sycophancy rule risks becoming “protect the advisor persona”.** Corrections should be truth-first: verify, acknowledge, update, explain.
22. **Four-dimensional pivot cost is mandatory even for trivial preference changes.** Pivot-cost dimensions must be conditional on the actual category/shape change.
23. **Default output is too wide.** Very large matrices obscure the decision and increase unsupported-field risk.
24. **No Pareto-before-score rule.** Weighted scoring can create false precision when one product is dominated or when weights are not actually known.
25. **No sensitivity analysis seam.** When top choices are close, the current system cannot state the preference threshold that flips the recommendation.
26. **No explicit degraded-mode contract.** If a key database is inaccessible, the skill needs a reproducible “blocked / partial evidence” behavior.

## P0 — Validation/evaluation defects

27. **No executable benchmark contract is bundled with the uploaded skill.**
28. **No immutable case identifiers or manifests.** Results cannot be reproduced or compared safely.
29. **No baseline/full-skill paired design.** Improvement cannot be attributed to the skill.
30. **No ablation protocol tied to feature-specific outcomes.**
31. **No positive control.** A broken evidence policy should be detectable by the evaluator.
32. **No sham/style control.** The evaluator may reward longer/prettier answers instead of better decisions.
33. **No blind review procedure.** Human raters can be biased by knowing which condition produced an answer.
34. **No repeated stochastic runs.** Single-run wins are fragile.
35. **No paired statistical analysis or confidence intervals.**
36. **No fixed release gate.** Teams can move the goalposts after seeing results.
37. **No distinction between product failure, evaluator failure, source unavailability, and protocol invalidity.**

## P1/P2 — Maintainability defects

38. **Category knowledge is monolithic rather than selectively loadable.**
39. **Volatile facts and stable research heuristics are mixed in the same references.**
40. **No last-verified/freshness discipline for references.**
41. **No source registry explaining permissible proof roles and access limitations.**
42. **No community-contribution schema for conflicts of interest, counterexamples, applicability, and expiry.**
43. **No cross-runtime capability matrix.** Web, subagent, scripting, and structured-output capabilities differ across agents.
44. **No activation regression test.** The skill can become too broad and trigger when it should not.

## Required direction

The next version must become a **claim-centric, product-identity-aware, risk-budgeted decision system** whose performance is demonstrated by real paired experiments. It must be able to say “unknown”, “disputed”, “not enough evidence”, and “blocked by source access” without treating those outcomes as failures to fill a template.
