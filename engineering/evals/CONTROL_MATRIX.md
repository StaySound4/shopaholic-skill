# Evaluator Control Matrix

| Control | Deliberate mutation | Metric expected to worsen | Metric that should NOT magically improve | Invalid if |
|---|---|---|---|---|
| Positive bad evidence | allow seller/marketing source to prove independent durability; allow unsupported claim as verified | unsupported-claim rate, source-role appropriateness, uncertainty honesty | hard constraints unrelated to evidence | evaluator cannot distinguish it from valid condition |
| Sham style | prettier headings, longer tables, polished tone only | none by design | evidence correctness, identity accuracy, hard constraints | reviewer strongly prefers sham on correctness/evidence without substantive difference |
| Risk overclaim mutation | treat one anecdote as product-wide veto/common defect | risk calibration | identity unrelated to risk | risk rubric does not penalize |
| Identity merge mutation | collapse CN/US or Rev A/B | identity accuracy, constraint compliance where affected | unrelated price arithmetic | exact identity scorer passes |
| Math mutation | add known arithmetic/flip-point error | deterministic math | prose style | deterministic test passes wrong value |

Controls are evaluator tests. If they fail, do not change the product to make the evaluator look good; repair the measurement system first.
