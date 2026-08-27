#!/usr/bin/env python3
"""Cross-border landed-cost, safety certifications, and regional compatibility engine.
Computes deterministic monetary landed costs (product + shipping + duty/tax) * FX,
strictly prohibits silently zeroing unknown taxes or shipping costs, verifies destination
electrical and safety certifications (UL, ETL, CSA, CE, PSE), discloses non-monetary
regional risks (voltage/plug, voided warranty, lack of 3C, cloud locks, return friction),
tracks overseas historical price tracking (Keepa logic), and filters ASIN review hijacking.
"""
from typing import Any, Dict, List, Optional

SELLER_FULFILLMENT_TIERS = {
    "sold_and_shipped_by_retailer", # Lowest risk: direct retailer first-party (e.g. Amazon.com Direct)
    "fulfilled_by_retailer_fba",    # Third-party seller with platform warehouse logistics
    "third_party_merchant_fbm"      # High risk: third-party merchant self-fulfillment
}

DESTINATION_CERTIFICATIONS = {"UL", "ETL", "CSA", "CE", "PSE", "FDA", "EPREL", "FCC"}

def calculate_cross_border_landed_cost(
    product_price: float,
    currency: str,
    fx_rate_to_cny: float,
    international_shipping: Optional[float] = None,
    import_duty_tax: Optional[float] = None,
    tax_status: str = "known",
    shipping_status: str = "known"
) -> Dict[str, Any]:
    """Calculates deterministic landed cost or safely flags unknown tax/shipping."""
    missing_shipping = shipping_status == "unknown" or international_shipping is None
    missing_tax = tax_status == "unknown" or import_duty_tax is None

    if missing_shipping or missing_tax:
        reasons = []
        if missing_shipping:
            reasons.append("international shipping cost is unknown")
        if missing_tax:
            reasons.append("import duty / customs tax is unknown")
        return {
            "is_complete": False,
            "currency": currency,
            "product_price": product_price,
            "international_shipping": international_shipping,
            "import_duty_tax": import_duty_tax,
            "tax_status": tax_status,
            "shipping_status": shipping_status,
            "landed_cost_cny": None,
            "fx_rate_to_cny": fx_rate_to_cny,
            "risk_warning": f"Landed cost cannot be calculated: {', and '.join(reasons)}; zero-cost assumptions are forbidden."
        }

    total_foreign = product_price + international_shipping + import_duty_tax
    landed_cny = round(total_foreign * fx_rate_to_cny, 2)

    return {
        "is_complete": True,
        "currency": currency,
        "product_price": product_price,
        "international_shipping": international_shipping,
        "import_duty_tax": import_duty_tax,
        "tax_status": tax_status,
        "shipping_status": shipping_status,
        "total_foreign_cost": total_foreign,
        "fx_rate_to_cny": fx_rate_to_cny,
        "landed_cost_cny": landed_cny,
        "risk_warning": None
    }

def verify_destination_safety_certifications(
    product_model: str,
    destination_region: str,
    claimed_certifications: List[str],
    official_registry_certs: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Verifies mandatory destination legal/safety certifications."""
    verified = []
    unverified = []
    official_set = set(official_registry_certs or [])
    
    for cert in claimed_certifications:
        c_upper = cert.upper()
        if c_upper in DESTINATION_CERTIFICATIONS and (official_registry_certs is None or c_upper in official_set):
            verified.append(c_upper)
        else:
            unverified.append(cert)
            
    is_compliant = len(verified) > 0 and len(unverified) == 0
    return {
        "product_model": product_model,
        "destination_region": destination_region,
        "verified_certifications": verified,
        "unverified_certifications": unverified,
        "is_safety_compliant": is_compliant
    }

def evaluate_cross_border_regional_risks(
    product_model: str,
    origin_market: str,             # "US", "JP", "EU", "UK"
    destination_market: str = "CN",
    voltage: Optional[str] = None,  # "110V", "100V", "220V-240V", "100V-240V_wide"
    plug_type: Optional[str] = None, # "Type A/B (US)", "Type G (UK)", "Type C/E/F (EU)"
    has_domestic_warranty: bool = False,
    has_domestic_3c: bool = False,
    has_regional_cloud_lock: bool = False,
    has_high_return_friction: bool = True,
    seller_tier: str = "sold_and_shipped_by_retailer",
    condition: str = "brand_new"    # "brand_new", "renewed_refurbished", "warehouse_open_box"
) -> Dict[str, Any]:
    """Evaluates non-monetary regional compatibility and channel risks."""
    risks = []
    
    # 1. Voltage & Electrical safety
    if voltage in ["110V", "100V"]:
        risks.append({
            "risk_type": "voltage_incompatibility",
            "severity": "critical_hardware_damage",
            "detail": f"Native {voltage} appliance requires dedicated step-down transformer for China 220V mains."
        })
    if plug_type and "Type G" in plug_type:
        risks.append({
            "risk_type": "plug_incompatibility",
            "severity": "low",
            "detail": f"Requires UK Type G to CN plug adapter."
        })

    # 2. Warranty and service
    if not has_domestic_warranty:
        risks.append({
            "risk_type": "voided_domestic_warranty",
            "severity": "high",
            "detail": "No official domestic warranty in China; requires international return shipping for repairs."
        })

    # 3. Regulatory Certification
    if not has_domestic_3c:
        risks.append({
            "risk_type": "missing_domestic_ccc",
            "severity": "medium",
            "detail": "Product lacks China Compulsory Certification (CCC) mark."
        })

    # 4. Regional Cloud Lock
    if has_regional_cloud_lock:
        risks.append({
            "risk_type": "regional_cloud_lock",
            "severity": "high",
            "detail": "Device features regional server geofencing or account region lock preventing domestic app use."
        })

    # 5. Return Friction
    if has_high_return_friction:
        risks.append({
            "risk_type": "high_cross_border_return_friction",
            "severity": "medium",
            "detail": "Cross-border return entails expensive international courier fees and customs clearance burden."
        })

    # 6. Seller Fulfillment Tier
    if seller_tier == "third_party_merchant_fbm":
        risks.append({
            "risk_type": "high_seller_fulfillment_friction",
            "severity": "medium",
            "detail": "Fulfilled by third-party merchant (FBM) with higher shipping loss/counterfeit risk."
        })

    # 7. Product Condition
    if condition != "brand_new":
        risks.append({
            "risk_type": "non_new_condition",
            "severity": "medium",
            "detail": f"Unit is {condition} (Amazon Renewed / Open Box), not factory sealed."
        })

    return {
        "product_model": product_model,
        "origin_market": origin_market,
        "destination_market": destination_market,
        "voltage": voltage,
        "condition": condition,
        "seller_tier": seller_tier,
        "risk_count": len(risks),
        "disclosed_risks": risks
    }

def analyze_overseas_price_history(
    current_list_price: float,
    claimed_original_msrp: float,
    historical_90day_median_price: float
) -> Dict[str, Any]:
    """Unmasks inflated list prices and artificial deal markups (Keepa/CamelCamelCamel logic)."""
    is_inflated = claimed_original_msrp > (historical_90day_median_price * 1.3)
    real_discount_pct = round((1.0 - (current_list_price / historical_90day_median_price)) * 100, 1)
    
    return {
        "current_price": current_list_price,
        "claimed_original_msrp": claimed_original_msrp,
        "historical_90day_median": historical_90day_median_price,
        "is_msrp_inflated": is_inflated,
        "true_discount_vs_90day_median_pct": real_discount_pct,
        "notes": "Fake discount markup detected" if is_inflated else "Normal promotional discount"
    }

def detect_asin_review_hijacking(
    current_product_asin: str,
    current_product_category: str,
    top_reviews: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Filters review hijacking / ASIN variation swapping where reviews belong to unrelated products."""
    hijacked_reviews = []
    legitimate_reviews = []
    
    for r in top_reviews:
        review_product = r.get("reviewed_product_name", "").lower()
        if review_product and current_product_category.lower() not in review_product:
            hijacked_reviews.append(r)
        else:
            legitimate_reviews.append(r)
            
    is_hijacked = len(hijacked_reviews) > 0
    return {
        "asin": current_product_asin,
        "is_review_hijacked": is_hijacked,
        "hijacked_review_count": len(hijacked_reviews),
        "legitimate_review_count": len(legitimate_reviews),
        "filtered_score_confidence": "low" if is_hijacked else "high"
    }

if __name__ == "__main__":
    print("Landed Cost Engine Module ready.")
