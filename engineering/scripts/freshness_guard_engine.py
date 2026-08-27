#!/usr/bin/env python3
"""Freshness guard engine for static references and temporal runtime facts.
Prevents stale standards, obsolete regulatory statuses (e.g. labeling active standards
like GB 4706.1-2024 as 'upcoming'), wrong standard code citations (e.g. IEEE 1788 vs 1789),
and expired temporal facts from being presented as current.
"""
import datetime
import re
from typing import Any, Dict, List, Optional, Tuple

KNOWN_STANDARDS_REGISTRY = {
    "GB 4706.1-2024": {
        "title": "Household and similar electrical appliances - Safety - Part 1: General requirements",
        "effective_date": "2026-08-01",
        "status": "active", # Active as of 2026-08-01
        "prohibited_obsolete_phrasing": ["upcoming", "draft", "future standard", "pending release"]
    },
    "GB 4706.1-2005": {
        "title": "Household and similar electrical appliances - Safety - Part 1: General requirements (Old)",
        "status": "superseded",
        "superseded_by": "GB 4706.1-2024"
    },
    "IEEE 1789-2015": {
        "title": "IEEE Recommended Practices for Modulating Current in High-Brightness LEDs for Mitigating Health Risks to Viewers",
        "status": "active",
        "prohibited_errata": ["IEEE 1788", "IEEE 1788-2015"]
    }
}

def resolve_dynamic_query_year(query_template: str, current_year: Optional[int] = None) -> str:
    """Replaces hardcoded temporal year tokens and static historical year literals with runtime year."""
    year = current_year if current_year is not None else datetime.date.today().year
    # Replace template placeholders
    resolved = query_template.replace("{{CURRENT_YEAR}}", str(year)).replace("{year}", str(year))
    # Replace explicit past year literals like 2024 or 2025 with dynamic current year
    resolved = re.sub(r"\b202[0-5]\b", str(year), resolved)
    return resolved

def audit_standard_citation(
    citation_text: str,
    target_standard_code: str,
    live_registry_status: Optional[str] = None
) -> Dict[str, Any]:
    """Audits a regulatory citation against known errata, superseded versions, and live registry status."""
    spec = KNOWN_STANDARDS_REGISTRY.get(target_standard_code)
    
    # 1. Check known code errata (e.g. IEEE 1788 instead of 1789)
    if spec and "prohibited_errata" in spec:
        for erratum in spec["prohibited_errata"]:
            if erratum.lower() in citation_text.lower():
                return {
                    "is_valid": False,
                    "target_standard": target_standard_code,
                    "error_type": "standard_code_erratum",
                    "correction": f"Confused '{erratum}' with correct standard '{target_standard_code}' (LED flicker mitigation).",
                    "corrected_text": citation_text.replace(erratum, target_standard_code)
                }

    # 2. Check superseded or repealed status
    effective_status = live_registry_status if live_registry_status else (spec["status"] if spec else "unknown")
    
    if effective_status == "superseded":
        successor = spec.get("superseded_by", "newer standard") if spec else "newer standard"
        return {
            "is_valid": False,
            "target_standard": target_standard_code,
            "error_type": "superseded_standard",
            "correction": f"Standard '{target_standard_code}' is SUPERSEDED by '{successor}'.",
            "status": "superseded",
            "successor": successor
        }

    if effective_status == "repealed":
        return {
            "is_valid": False,
            "target_standard": target_standard_code,
            "error_type": "repealed_standard",
            "correction": f"Standard '{target_standard_code}' has been REPEALED/withdrawn.",
            "status": "repealed"
        }

    # 3. Check obsolete status phrasing (e.g. GB 4706.1-2024 upcoming)
    if spec and effective_status == "active":
        for obsolete_phrase in spec.get("prohibited_obsolete_phrasing", []):
            if obsolete_phrase.lower() in citation_text.lower():
                return {
                    "is_valid": False,
                    "target_standard": target_standard_code,
                    "error_type": "obsolete_status_phrasing",
                    "correction": f"Standard '{target_standard_code}' is currently ACTIVE (effective {spec.get('effective_date')}); obsolete phrasing '{obsolete_phrase}' removed.",
                    "status": "active"
                }

    return {
        "is_valid": True,
        "target_standard": target_standard_code,
        "error_type": None,
        "status": effective_status
    }

def evaluate_reference_freshness(
    reference_id: str,
    published_date_str: str,
    is_timeless_physics: bool = False,
    current_date_str: Optional[str] = None,
    ttl_days: int = 180
) -> Dict[str, Any]:
    """Evaluates reference age dynamically; timeless physics remain undated and valid."""
    if is_timeless_physics:
        return {
            "reference_id": reference_id,
            "is_fresh": True,
            "confidence_grade": "S",
            "reason": "Timeless physical/acoustical/optical principle; exempt from temporal TTL."
        }

    pub_date = datetime.date.fromisoformat(published_date_str)
    cur_date = datetime.date.fromisoformat(current_date_str) if current_date_str else datetime.date.today()
    age_days = (cur_date - pub_date).days

    if age_days > ttl_days:
        return {
            "reference_id": reference_id,
            "is_fresh": False,
            "age_days": age_days,
            "confidence_grade": "B", # Degrade stale reference
            "requires_reverification": True,
            "reason": f"Reference is {age_days} days old (exceeds TTL of {ttl_days} days)."
        }

    return {
        "reference_id": reference_id,
        "is_fresh": True,
        "age_days": age_days,
        "confidence_grade": "S",
        "requires_reverification": False,
        "reason": "Fresh reference within TTL."
    }

if __name__ == "__main__":
    print("Freshness Guard Engine ready.")
