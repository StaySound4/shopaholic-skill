#!/usr/bin/env python3
"""Origin and temporal semantics engine with inference shortcut prohibitions.
Prevents illegitimate origin assumptions (GTIN license prefix != manufacturing origin,
brand HQ != assembly country), tracks decoupled temporal dates, and verifies regulatory standard status.
"""
import argparse, datetime, json, re, sys
from pathlib import Path

def resolve_manufacturing_origin(
    brand_hq_country: str | None = None,
    gtin_prefix_country: str | None = None,
    physical_nameplate_country: str | None = None,
    certificate_factory_country: str | None = None
) -> dict:
    """Determines manufacturing and assembly country without inference shortcuts.
    Invariant: Neither GTIN country nor Brand HQ country can be used to assert 'Made in X'.
    """
    if physical_nameplate_country:
        origin = physical_nameplate_country
        source = "physical_nameplate"
        confidence = "verified"
    elif certificate_factory_country:
        origin = certificate_factory_country
        source = "regulatory_factory_certificate"
        confidence = "verified"
    else:
        origin = None
        source = "unknown"
        confidence = "unverified"
        
    return {
        "country_of_origin": origin,
        "assembly_country": origin,
        "source": source,
        "confidence": confidence,
        "gtin_prefix_country": gtin_prefix_country,
        "brand_hq_country": brand_hq_country,
        "shortcut_prevented": (origin is None and (gtin_prefix_country is not None or brand_hq_country is not None))
    }

def structure_product_lifecycle_dates(
    announcement_date: str | None = None,
    first_sale_date: str | None = None,
    regional_first_sale_date: str | None = None,
    certification_date: str | None = None,
    revision_start_date: str | None = None,
    batch_window: str | None = None,
    eol_date: str | None = None
) -> dict:
    """Structures decoupled product lifecycle dates."""
    return {
        "announcement_date": announcement_date,
        "first_sale_date": first_sale_date,
        "regional_first_sale_date": regional_first_sale_date,
        "certification_date": certification_date,
        "revision_start_date": revision_start_date,
        "batch_window": batch_window,
        "eol_date": eol_date
    }

def verify_standard_temporal_status(
    standard_code: str,
    reference_date: datetime.date | None = None,
    registry_data: dict | None = None
) -> dict:
    """Evaluates regulatory standard temporal status against reference date."""
    ref_date = reference_date or datetime.date.today()
    
    # Check if we have authoritative registry data
    if registry_data and standard_code in registry_data:
        info = registry_data[standard_code]
        implementation_date_str = info.get("implementation_date")
        superseded_date_str = info.get("superseded_date")
        
        status = "active"
        if implementation_date_str:
            imp_date = datetime.date.fromisoformat(implementation_date_str)
            if ref_date < imp_date:
                status = "upcoming"
        if superseded_date_str:
            sup_date = datetime.date.fromisoformat(superseded_date_str)
            if ref_date >= sup_date:
                status = "superseded"
                
        return {
            "standard_code": standard_code,
            "status": status,
            "reference_date": ref_date.isoformat(),
            "standard_title": info.get("title")
        }
        
    return {
        "standard_code": standard_code,
        "status": "unverified",
        "reference_date": ref_date.isoformat(),
        "notes": "No registry record available"
    }

def get_dynamic_runtime_year(runtime_date_str: str | None = None) -> int:
    """Derives current-year dynamic queries from runtime date without static literals."""
    if runtime_date_str:
        return datetime.date.fromisoformat(runtime_date_str).year
    return datetime.date.today().year

if __name__ == "__main__":
    print("Origin and Temporal Engine ready.")
