#!/usr/bin/env python3
"""Four-level product entity resolution engine.
Resolves Canonical Product -> Region SKU -> Revision -> Batch hierarchy,
enforces jurisdiction-specific compliance isolation (3C, FCC ID, CE, PSE),
and binds claims to the narrowest evidence-supported identity scope.
"""
import argparse, json, sys, uuid
from pathlib import Path

def resolve_product_entity(
    brand: str,
    model_name: str,
    model_code: str | None = None,
    region_sku: str | None = None,
    region: str | None = None,
    revision: str | None = None,
    batch: str | None = None,
    identifiers: dict | None = None,
    dates: dict | None = None,
    provenance: dict | None = None,
    certifications: list[dict] | None = None,
    physical_verification_rule: str | None = None,
    evidence_refs: list[str] | None = None
) -> dict:
    """Constructs a fully resolved 4-level product entity record."""
    entity_id = f"PROD-{brand.upper().replace(' ', '')}-{model_name.upper().replace(' ', '')}"
    if region_sku:
        entity_id += f"-{region_sku}"
    if revision:
        entity_id += f"-{revision.replace(' ', '')}"
    if batch:
        entity_id += f"-{batch.replace(' ', '')}"
        
    return {
        "entity_id": entity_id,
        "canonical_product": {
            "brand": brand,
            "model_name": model_name,
            "model_code": model_code
        },
        "region_sku": region_sku,
        "region": region,
        "revision": revision,
        "batch": batch,
        "identifiers": identifiers or {},
        "dates": dates or {},
        "provenance": provenance or {},
        "certifications": certifications or [],
        "physical_verification_rule": physical_verification_rule,
        "identity_confidence": "high" if (brand and model_name) else "medium",
        "evidence_refs": evidence_refs or []
    }

def match_bundle_to_canonical(bundle_name: str, known_canonical_products: list[dict]) -> dict | None:
    """Resolves a retail package/bundle variation to its canonical host product."""
    b_lower = bundle_name.lower()
    for prod in known_canonical_products:
        brand = prod.get("brand", "").lower()
        model = prod.get("model_name", "").lower()
        if brand in b_lower and model in b_lower:
            return prod
    return None

def check_feature_inheritance_across_revisions(
    claim_text: str,
    source_revision: str,
    target_revision: str,
    revision_changelog: dict | None = None
) -> bool:
    """Determines whether a claim from source_revision can be inherited by target_revision.
    If the changelog indicates the feature/hardware was altered or removed, inheritance is forbidden.
    """
    if source_revision == target_revision:
        return True
        
    if revision_changelog:
        removed_features = revision_changelog.get("removed_features", [])
        changed_components = revision_changelog.get("changed_components", [])
        
        claim_lower = claim_text.lower()
        for rem in removed_features:
            if rem.lower() in claim_lower:
                return False
        for chg in changed_components:
            if chg.lower() in claim_lower:
                return False
                
    # By default, claims must not be blindly inherited across distinct hardware revisions
    return False

if __name__ == "__main__":
    print("Product Entity Resolver Module ready.")
