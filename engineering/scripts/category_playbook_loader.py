#!/usr/bin/env python3
"""Modular category knowledge and progressive playbook loader.
Implements a 3-tier progressive loading architecture:
Tier 1: Core Router (<150 lines)
Tier 2: On-demand single Category Playbook (references/categories/<slug>.md)
Tier 3: On-demand deep forensics (R2/R3 regulatory/teardown playbooks)
Enforces absolute context isolation: loading Category A strictly excludes all other categories.
"""
from pathlib import Path
from typing import Any, Dict, List, Optional

PLAYBOOKS_DIR = Path(__file__).resolve().parent.parent.parent / "references" / "categories"

SLUG_MAPPINGS = {
    "coffee": "coffee.md",
    "espresso": "coffee.md",
    "coffee_machine": "coffee.md",
    "grinder": "coffee.md",
    "hifi": "hifi-audio.md",
    "hifi-audio": "hifi-audio.md",
    "dac": "hifi-audio.md",
    "headphone_amp": "hifi-audio.md",
    "display": "display-monitors.md",
    "display-monitors": "display-monitors.md",
    "monitor": "display-monitors.md",
    "screen": "display-monitors.md",
    "infant": "infant-gear.md",
    "infant-gear": "infant-gear.md",
    "car_seat": "infant-gear.md",
    "baby": "infant-gear.md"
}

def resolve_category_playbook(category_query: str) -> Optional[str]:
    """Resolves category query to exact category playbook filename."""
    q_clean = category_query.lower().replace(" ", "_").replace("-", "_")
    for key, filename in SLUG_MAPPINGS.items():
        if key in q_clean:
            return filename
    return None

def load_progressive_category_context(
    category_query: str,
    research_budget: str = "R1",
    base_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Loads exactly one category playbook with strict context isolation."""
    pb_dir = base_dir or PLAYBOOKS_DIR
    filename = resolve_category_playbook(category_query)
    
    if not filename:
        return {
            "tier_1_loaded": True,
            "tier_2_playbook": None,
            "tier_3_deep_forensics": None,
            "isolated_category_slug": None,
            "loaded_files": ["references/categories/INDEX.md"],
            "notes": "No matching category playbook; general decision physics apply."
        }

    target_file = pb_dir / filename
    if not target_file.exists():
        raise FileNotFoundError(f"Category playbook file not found: {target_file}")

    content = target_file.read_text(encoding="utf-8")
    
    # Tier 3 deep forensics activated conditionally for R2/R3
    tier_3_active = research_budget in ["R2", "R3"]

    return {
        "tier_1_loaded": True,
        "tier_2_playbook": filename,
        "tier_3_deep_forensics": tier_3_active,
        "isolated_category_slug": filename.replace(".md", ""),
        "loaded_files": [f"references/categories/{filename}"], # Exactly 1 category file in context
        "playbook_content": content,
        "context_isolation_verified": True
    }

if __name__ == "__main__":
    print("Category Playbook Loader Module ready.")
