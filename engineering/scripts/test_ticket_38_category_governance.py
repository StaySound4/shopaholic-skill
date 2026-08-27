#!/usr/bin/env python3
"""Test suite for Ticket 38: Govern community category contributions.
Tests:
1. Pass: Compliant 12-section category playbook with standards, commercial disclosures, counterexamples, and metadata passes cleanly.
2. Adversarial: Missing commercial conflict disclosure is rejected.
3. Adversarial: Missing falsifiable counterexamples is rejected.
4. Adversarial: Unanchored static Top-10 rankings or hardcoded prices are rejected.
5. Adversarial: Missing maintainer / last_reviewed_at metadata is rejected.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_category_playbook import (
    validate_category_playbook_content
)

VALID_SAMPLE_PLAYBOOK = """
# Category Playbook: Espresso Machines

## Category scope
Covers consumer espresso machines. Excludes commercial multi-group cafe units.

## Stable decision physics / mechanisms
- Thermoblock vs Dual Boiler heating stability tradeoffs.

## Hard safety / compatibility variables
- GB 4706.1-2024 Household Electrical Safety (Active)
- GB 4806.9 Food Contact Metallic Materials
- CE / UL 1082

## User-declared hard constraints commonly encountered
- Available kitchen counter clearance.

## Measurements that matter
- Temperature stability under brew load (+/- 1.5 deg C).

## Marketing claims requiring skepticism
- Unmask false 'commercial rotary pump' claims when units contain vibratory pumps.

## Failure hypotheses and field signals
- Counterexample: Dual boilers are superior for back-to-back milk drinks, but fail and overheat when used in unventilated compact spaces (boundary limit: requires 10cm clearance).

## Version / region / batch concerns
- China 3C vs US 120V 60Hz heating element batch differences.

## Category-specific search / evidence playbooks
- `espresso machine boiler safety recall {{CURRENT_YEAR}}`

## Degraded operation
- When CNCA database is offline, fall back to independent teardown reports with grade B.

## Commercial relationships & conflicts of interest
Commercial disclosure: None. The author has no financial affiliations or sponsorships with espresso brands.

## Review metadata
- maintainer: CoffeeResearchTeam
- last_reviewed_at: 2026-08-28
"""

class TestTicket38CategoryGovernance(unittest.TestCase):
    def test_01_valid_playbook_passes_all_checks(self):
        """Pass path: Fully compliant 12-section playbook passes validation."""
        res = validate_category_playbook_content(VALID_SAMPLE_PLAYBOOK)
        self.assertTrue(res["is_valid"])
        self.assertEqual(len(res["errors"]), 0)
        self.assertIsNone(res["remediation_guidance"])

    def test_02_adversarial_missing_commercial_disclosure_rejected(self):
        """Adversarial path: Omitting commercial conflict statement triggers rejection."""
        bad_text = VALID_SAMPLE_PLAYBOOK.replace(
            "Commercial disclosure: None. The author has no financial affiliations or sponsorships with espresso brands.",
            "This section is left blank."
        )
        res = validate_category_playbook_content(bad_text)
        self.assertFalse(res["is_valid"])
        self.assertTrue(any("Commercial disclosure" in e for e in res["errors"]))

    def test_03_adversarial_missing_counterexample_rejected(self):
        """Adversarial path: Omitting falsifiable counterexamples triggers rejection."""
        bad_text = VALID_SAMPLE_PLAYBOOK.replace(
            "Counterexample: Dual boilers are superior for back-to-back milk drinks, but fail and overheat when used in unventilated compact spaces (boundary limit: requires 10cm clearance).",
            "Everything is great and always works unconditionally."
        )
        res = validate_category_playbook_content(bad_text)
        self.assertFalse(res["is_valid"])
        self.assertTrue(any("counterexample" in e.lower() for e in res["errors"]))

    def test_04_adversarial_unanchored_top10_and_prices_rejected(self):
        """Adversarial path: Unanchored Top 10 rankings or hardcoded unverified fixed prices trigger rejection."""
        bad_text_top10 = VALID_SAMPLE_PLAYBOOK + "\n## Extra\nTop 10 best products of all time list."
        res1 = validate_category_playbook_content(bad_text_top10)
        self.assertFalse(res1["is_valid"])
        self.assertTrue(any("Top 10" in e for e in res1["errors"]))

        bad_text_price = VALID_SAMPLE_PLAYBOOK + "\n## Extra\nFixed price: 2999 RMB"
        res2 = validate_category_playbook_content(bad_text_price)
        self.assertFalse(res2["is_valid"])
        self.assertTrue(any("Fixed price" in e or "hardcoded" in e for e in res2["errors"]))

    def test_05_adversarial_missing_metadata_rejected(self):
        """Adversarial path: Missing maintainer or invalid last_reviewed_at triggers rejection."""
        bad_text = VALID_SAMPLE_PLAYBOOK.replace("- maintainer: CoffeeResearchTeam", "")
        res = validate_category_playbook_content(bad_text)
        self.assertFalse(res["is_valid"])
        self.assertTrue(any("maintainer" in e.lower() for e in res["errors"]))

if __name__ == "__main__":
    unittest.main()
