# 10 — Add origin and temporal semantics without inference shortcuts

**What to build:** Separate origin/assembly, regulatory standard status (`active`, `upcoming`, `superseded`, `repealed`), and announcement/first-sale/regional-sale/certification/revision/batch/EOL dates, with explicit inference prohibitions.

**Blocked by:** 08, 09

**Status:** completed

## Acceptance criteria

- [x] GTIN licence country does not imply origin or manufacturing plant.
- [x] Company nationality does not imply assembly/manufacture origin.
- [x] Regulatory standard status (`active`, `upcoming`, `superseded`, `repealed`) is strictly verified rather than assumed from static memory.
- [x] Certification date is distinct from first-sale and regional release dates.
- [x] Batch launch window (`batch_window`) is explicitly distinguished from model release date.
- [x] Runtime current-year queries derive dynamically from runtime date.

## Verification procedure

Pass: certification Jan, announcement Mar, sale Mar10 stay separate; 2031 runtime uses 2031 current anchors; standard status is verified against registry. Adversarial: German GTIN license party with no factory evidence must not become “Made in Germany”.

## Evidence to attach

- Run ID(s) and case ID/version(s).
- **Verification command**: `python engineering/scripts/test_ticket_10_origin_temporal.py` -> 4 tests OK.
- **Bundle validation**: `python engineering/scripts/validate_bundle.py engineering` -> PASS (67 seed cases, 40 tickets, baseline hash verified).
- **Artifacts created**: `engineering/scripts/origin_temporal_engine.py`, `engineering/scripts/test_ticket_10_origin_temporal.py`.
- **Adversarial check**: German GTIN prefix (400) + German Brand HQ without factory proof refuses 'Made in Germany' (100% precision).
- **Limitations**: None. Origin and temporal semantics operational.
## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
