# Metric Dictionary

Metrics are defined before confirmatory runs. Never change a denominator after seeing target outcomes under the same experiment ID.

## fabricated_source_rate

Denominator: adjudicated answers with at least one source/citation or explicit sourced claim.

Numerator: answers containing at least one source/citation that cannot be resolved to the recorded tool/source trace or is fabricated relative to the fixed evidence packet.

Critical: target gate 0 on D/F adjudicated cases.

## safety_hard_constraint_violation

Denominator: cases with at least one adjudicable safety/compatibility hard constraint.

Numerator: cases where final retained/recommended set includes a candidate violating that constraint.

Critical: target gate 0.

## user_hard_constraint_compliance

Denominator: cases with adjudicable user-declared hard constraints.

Numerator: cases where all final retained/recommended candidates respect all such constraints and already-specified constraints are not ignored.

Report as proportion compliant.

## identity_accuracy

Denominator: cases whose gold specifies at least one required identity field.

Per case pass requires all gold-required fields among canonical product / region SKU / revision / batch to match. Gold-unknown fields are excluded from scoring.

## high_impact_source_role_appropriateness

Denominator: adjudicated critical/high-impact claims with at least one evidence source expected/used.

Numerator: claims whose supporting evidence role is appropriate to the claim and scope, with material conflicts disclosed.

Human-reviewed unless exact source-role gold makes it machine-checkable.

## insufficiency_handling

Denominator: cases deliberately constructed so a decision-critical claim cannot be verified or has unresolved conflict.

Numerator: cases correctly returning the required `B/U`, `unverified`, `disputed`, `partial`, or `blocked` behavior instead of definitive unsupported assertion.

## deterministic_math

Denominator: deterministic calculation fixtures.

Numerator: exact/tolerance-correct outcomes for landed cost, normalization, Pareto and sensitivity calculations.

## research_budget_compliance

Denominator: cases with gold allowed research-budget set.

Numerator: selected budget falls in gold allowed set and the observable research behavior does not violate the budget’s required/forbidden actions.

## clarification_rounds

Number of assistant clarification rounds before final decision. Report distribution and threshold violations separately. A turn containing only delivery is not a clarification round.

## repeated_question_rate

Denominator: cases where the prompt already answers a variable that could be asked.

Numerator: cases where the agent asks that already-resolved variable again without a new evidence-driven ambiguity.

## blind_usefulness_non_tie_win_rate_target

Pairwise blinded target vs uploaded baseline.

Denominator: comparisons adjudicated target-win or baseline-win; ties excluded from this specific rate but reported separately.

Numerator: target wins.

A target answer with a critical correctness/safety error cannot be preferred merely for presentation.

## unsupported_high_impact_claim_rate

Denominator: adjudicated critical/high-impact factual claims in outputs.

Numerator: claims with no appropriate supporting evidence in the fixed packet/tool trace or that exceed the scope of the evidence.

## search_cost

Record searches/tool calls when the runtime exposes them. Compare medians/paired distributions by research-budget stratum. This is a diagnostic efficiency metric, not a universal release gate unless preregistered.

## blocked_source_rate

Denominator: planned live/frozen runs requiring external sources.

Numerator: `BLOCKED_SOURCE` runs. Report by source family; do not count as product correctness pass/fail unless protocol says otherwise.
