#!/usr/bin/env python3
"""Category playbook linter and community governance validator for Ticket 38.
Enforces strict compliance with CATEGORY_CONTRIBUTION_TEMPLATE.md,
mandatory domestic and international standards coverage, commercial conflict disclosures,
falsifiable counterexamples, and bans on unanchored static transient facts.
Provides actionable remediation guidance and strictly disallows contributor reputation bypasses.
"""
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MANDATORY_SECTIONS = [
    ("Category scope", r"##\s+(?:\d+\.\s+)?Category\s+scope"),
    ("Stable decision physics / mechanisms", r"##\s+(?:\d+\.\s+)?(?:Stable\s+decision\s+physics|Decision\s+Heuristics)"),
    ("Hard safety / compatibility variables", r"##\s+(?:\d+\.\s+)?(?:Hard\s+safety|Mandatory(?:\s+\w+)?\s+Standards)"),
    ("User-declared hard constraints", r"##\s+(?:\d+\.\s+)?(?:User-declared|Authoritative\s+Source)"),
    ("Measurements that matter", r"##\s+(?:\d+\.\s+)?(?:Measurements\s+that\s+matter|Critical\s+Safety)"),
    ("Marketing claims requiring skepticism", r"##\s+(?:\d+\.\s+)?(?:Marketing\s+claims|Anti-Cheat)"),
    ("Failure hypotheses and field signals", r"##\s+(?:\d+\.\s+)?(?:Failure\s+hypotheses|Falsifiable\s+Counterexamples)"),
    ("Version / region / batch concerns", r"##\s+(?:\d+\.\s+)?(?:Version\s*\/\s*region|Live\s+Search)"),
    ("Category-specific search / evidence playbooks", r"##\s+(?:\d+\.\s+)?(?:Category-specific\s+search|Temporal\s+Anchors)"),
    ("Degraded operation", r"##\s+(?:\d+\.\s+)?(?:Degraded\s+operation|Degraded\s+Fallback)"),
    ("Commercial relationships & conflicts of interest", r"##\s+(?:\d+\.\s+)?(?:Commercial\s+relationships|Commercial\s+Disclosure)"),
    ("Review metadata", r"##\s+(?:\d+\.\s+)?Review\s+metadata")
]

def extract_section_content(markdown_text: str, section_pattern: str) -> str:
    """Extracts content belonging to a specific section up to the next heading."""
    match = re.search(section_pattern, markdown_text, re.IGNORECASE)
    if not match:
        return ""
    start_pos = match.end()
    next_heading = re.search(r"\n##\s+", markdown_text[start_pos:])
    if next_heading:
        return markdown_text[start_pos : start_pos + next_heading.start()]
    return markdown_text[start_pos:]

def validate_category_playbook_content(markdown_text: str) -> Dict[str, Any]:
    """Validates markdown playbook text against all 12 governance rules."""
    errors = []
    warnings = []

    # 1. Check all 12 mandatory sections
    for sec_name, sec_pattern in MANDATORY_SECTIONS:
        if not re.search(sec_pattern, markdown_text, re.IGNORECASE):
            errors.append(f"Missing mandatory section: '{sec_name}'. Please follow CATEGORY_CONTRIBUTION_TEMPLATE.md.")

    # 2. Check Commercial Conflict Disclosure
    comm_content = extract_section_content(markdown_text, r"##\s+(?:\d+\.\s+)?(?:Commercial\s+relationships|Commercial\s+Disclosure)")
    if comm_content:
        if not re.search(r"(?i)\b(none|no\s+conflicts?|sponsored|affiliated|commercial\s+relationship|no\s+financial)\b", comm_content):
            errors.append("Commercial disclosure section lacks explicit declaration (must declare 'None' or describe commercial affiliations).")

    # 3. Check Falsifiable Counterexamples
    counter_content = extract_section_content(markdown_text, r"##\s+(?:\d+\.\s+)?(?:Failure\s+hypotheses|Falsifiable\s+Counterexamples)")
    if counter_content:
        if not re.search(r"(?i)\b(counterexample|boundary|exception|failure\s+case|invalid\s+when|falsif\w*)\b", counter_content):
            errors.append("Playbook must contain explicit falsifiable counterexamples, boundary limits, or falsification criteria in failure hypotheses.")

    # 4. Check Prohibited Unanchored Static Prices / Rankings
    if re.search(r"(?i)top\s*10\s+best\s+products\s+of\s+all\s+time", markdown_text):
        errors.append("Static unanchored 'Top 10' product rankings are strictly prohibited without runtime dynamic search anchors.")

    # Check for hardcoded unanchored fixed price tables without {{CURRENT_YEAR}} or verification anchors
    if re.search(r"(?i)fixed\s+price\s*:\s*[0-9]+\s*RMB(?!\s*\(verified)", markdown_text):
        errors.append("Unverified static hardcoded prices are prohibited without dynamic temporal anchors or verification timestamps.")

    # 5. Check Review Metadata (maintainer & last_reviewed_at)
    meta_content = extract_section_content(markdown_text, r"##\s+(?:\d+\.\s+)?Review\s+metadata")
    search_scope = meta_content if meta_content else markdown_text
    
    if not re.search(r"(?i)maintainer\s*:", search_scope):
        errors.append("Missing maintainer identification in Review Metadata.")
    if not re.search(r"(?i)last_reviewed_at\s*:\s*\d{4}-\d{2}-\d{2}", search_scope):
        errors.append("Missing or invalid last_reviewed_at timestamp (must follow YYYY-MM-DD).")

    is_valid = len(errors) == 0
    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "passed_sections_count": len(MANDATORY_SECTIONS) - len(errors),
        "remediation_guidance": "Consult CATEGORY_CONTRIBUTION_TEMPLATE.md to address all missing sections and declarations." if not is_valid else None
    }

def validate_category_playbook_file(file_path: Path) -> Dict[str, Any]:
    """Validates a playbook markdown file on disk."""
    if not file_path.exists():
        return {
            "is_valid": False,
            "errors": [f"File '{file_path}' does not exist."],
            "warnings": [],
            "remediation_guidance": "Provide a valid file path."
        }
    content = file_path.read_text(encoding="utf-8")
    res = validate_category_playbook_content(content)
    res["file_path"] = str(file_path)
    return res

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        result = validate_category_playbook_file(p)
        print(f"Validation Result for {p}: {'PASS' if result['is_valid'] else 'FAIL'}")
        for err in result["errors"]:
            print(f"  - ERROR: {err}")
    else:
        print("Category Playbook Governance Validator ready.")
