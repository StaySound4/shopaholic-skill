# Traceability Matrix

This matrix is the audit spine from specification to implementation ticket to measurable evidence.

| Spec behavior | Primary tickets | Seed cases / experiment evidence |
|---|---|---|
| Baseline freeze & executable evaluation seam | 01 | baseline hashes & run-record smoke |
| Machine-readable cases & immutable manifests | 02 | manifest hash locking & case schemas |
| Evaluator positive & sham controls | 03 | C_positive_bad_evidence, C_sham_style |
| User hard constraints can exclude | 04, 15 | D-001, D-002, D-003, D-004 |
| Global evidence separate from purchase market | 14, 19 | D-005, D-006, L-001, D-046 |
| Product -> region -> revision -> batch identity | 08, 10 | D-007, D-011, D-012, D-013, D-020, D-047 |
| Provenance roles separated & OEM tracing | 09, 22, 23 | D-014, D-045, F-002 |
| No false origin inference & gray market risks | 09, 10, 19, 22 | D-015, D-046, F-002 |
| OEM same-platform requires strong identity anchors | 08, 09, 22, 23 | D-016, D-017, D-045, F-001 |
| Claim-centric evidence / conflict / unknown | 05, 06, 07 | D-008, D-009, D-010 |
| Commercial relationships recorded | 23 | D-008, D-009, D-045 + reviewer fixtures |
| Risk signal != prevalence | 13 | D-018, D-019, D-020, F-004, L-003 |
| Research effort adapts R0-R3 with discovery headroom | 11, 12, 15 | D-021, D-022, D-023, D-041 |
| Dynamic candidate count & dual-track delivery | 12, 20, 21 | D-040, D-044 |
| Current vs historical price semantics | 18 | D-024, D-025 |
| Cross-border landed cost & gray market risks | 19 | D-026, D-046 |
| Used/discontinued is conditional/category-aware | 16, 17 | D-004, D-027, D-028, D-043 |
| Max-three-round adaptive UX & pure intake | 15, 16 | D-029, D-030, D-041, D-042, D-043 |
| Pareto-first ranking | 24 | D-032 + added ranking fixtures |
| Deterministic sensitivity & scenario sliders | 25, 31 | D-031, D-032, D-048 |
| Conditional pivot-cost analysis | 26 | D-033, D-034 |
| Retrieved-content prompt injection resistance | 29 | D-035 |
| Explicit degraded mode | 30 | D-036 |
| Runtime temporal freshness | 10, 33 | D-037, D-038 |
| Category-specific evidence profiles | 27 | D-039 |
| Authoritative source routing | 22 | F-001..F-004, L-001..L-004 |
| Truth-first correction | 28 | dedicated beta correction cases |
| Automated scoring from real outputs | 31 | scorer mutation tests + every run record |
| Blinded human review | 32 | human-review seed cases and pairwise packets |
| Real paired experiment | 34, 35 | preregistered experiment dossier |
| Fixed release gates | 36 | gate report from experiment summary |
| Honest multi-runtime support | 37, 39 | cross-runtime critical suite |
| Community/freshness governance | 27, 33, 38 | contribution review artifacts |
| Public measured-improvement claims | 40 | v1 evidence dossier only |
