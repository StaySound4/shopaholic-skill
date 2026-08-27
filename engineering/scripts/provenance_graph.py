#!/usr/bin/env python3
"""Provenance and corporate-role graph engine.
Models 10 distinct corporate/supply-chain roles without conflation,
strictly separates proprietary OEM manufacturing from public-tooling rebadging,
and unmasks gray market / export-return channel risks.
"""
import argparse, json, sys
from pathlib import Path

VALID_CORPORATE_ROLES = [
    "brand_owner",
    "trademark_owner",
    "regulatory_applicant",
    "manufacturer",
    "factory",
    "odm_oem",
    "importer",
    "distributor",
    "seller",
    "parent_company"
]

def build_provenance_graph(
    role_assignments: dict[str, dict],
    upstream_odm_oem: str | None = None,
    upstream_base_price: float | None = None,
    current_retail_price: float | None = None,
    is_proprietary_tooling: bool = True,
    channel_type: str = "authorized"
) -> dict:
    """Builds a verified provenance graph across distinct corporate entities."""
    roles = {}
    for role_name in VALID_CORPORATE_ROLES:
        info = role_assignments.get(role_name)
        if info:
            roles[role_name] = {
                "entity_name": info.get("name"),
                "jurisdiction": info.get("jurisdiction"),
                "evidence_source_ref": info.get("evidence_source_ref")
            }
        else:
            roles[role_name] = None
            
    # Adjudicate rebadging type
    rebadging_type = "none"
    rebadge_unmasked = None
    
    if upstream_odm_oem:
        if is_proprietary_tooling:
            rebadging_type = "proprietary_oem"
        else:
            rebadging_type = "public_tooling_rebadge"
            markup_pct = 0.0
            if upstream_base_price and current_retail_price and upstream_base_price > 0:
                markup_pct = round((current_retail_price - upstream_base_price) / upstream_base_price * 100, 2)
            
            rebadge_unmasked = {
                "original_odm_oem": upstream_odm_oem,
                "upstream_base_price": upstream_base_price,
                "current_retail_price": current_retail_price,
                "estimated_markup_percentage": markup_pct,
                "excessive_markup_flag": markup_pct >= 30.0
            }
            
    # Channel risk classification
    channel_risks = []
    if channel_type == "parallel_import":
        channel_risks.append("parallel_import_gray_market: Potential voltage mismatch, lack of domestic 3C, voided official warranty.")
    elif channel_type == "export_return":
        channel_risks.append("export_return: Factory surplus/export-return goods lacking domestic warranty service.")
    elif channel_type == "oem_bulk_pack":
        channel_risks.append("oem_bulk_pack: Industrial bulk pack lacking retail packaging and end-user RMA.")

    return {
        "roles": roles,
        "rebadging_type": rebadging_type,
        "rebadge_unmasked": rebadge_unmasked,
        "channel_type": channel_type,
        "channel_risks": channel_risks
    }

def handle_entity_conflict(
    regulatory_manufacturer: str,
    marketing_story_brand: str,
    evidence_regulatory: str,
    evidence_marketing: str
) -> dict:
    """Handles conflict when marketplace marketing story disagrees with regulatory certification records."""
    if regulatory_manufacturer != marketing_story_brand:
        return {
            "conflict_detected": True,
            "resolved_manufacturer": regulatory_manufacturer,
            "marketing_brand_claim": marketing_story_brand,
            "status": "regulatory_authority_preserved",
            "reason": f"Regulatory certification record from {evidence_regulatory} holds legal authority over marketplace story in {evidence_marketing}."
        }
    return {"conflict_detected": False, "resolved_manufacturer": regulatory_manufacturer}

if __name__ == "__main__":
    print("Provenance Graph Module ready.")
