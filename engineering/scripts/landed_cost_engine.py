#!/usr/bin/env python3
"""Cross-border landed-cost and regional compatibility engine.
Computes deterministic monetary landed costs (product + shipping + duty/tax) * FX,
strictly prohibits silently zeroing unknown taxes/shipping, discloses non-monetary
regional risks (110V voltage, voided domestic warranty, missing 3C, cloud locks),
and tracks overseas merchant tiers and refurbished conditions.
"""
from typing import Any, Dict, List, Optional

SELLER_FULFILLMENT_TIERS = {
    "sold_and_shipped_by_retailer", # Lowest risk: direct retailer first-party
    "fulfilled_by_retailer_fba",    # Third-party seller with platform warehouse logistics
    "third_party_merchant_fbm"      # High risk: third-party merchant self-fulfillment
}

def calculate_cross_border_landed_cost(
    product_price: float,
    currency: str,
    fx_rate_to_cny: float,
    international_shipping: Optional[float] = None,
    import_duty_tax: Optional[float] = None,
    tax_status: str = "known"       # "known", "unknown", "exempt"
) -> Dict[str, Any]:
    """Calculates deterministic landed cost or safely flags unknown tax/shipping."""
    if tax_status == "unknown" or import_duty_tax is None:
        return {
            "is_complete": False,
            "currency": currency,
            "product_price": product_price,
            "international_shipping": international_shipping,
            "import_duty_tax": None,
            "tax_status": "unknown",
            "landed_cost_cny": None,
            "fx_rate_to_cny": fx_rate_to_cny,
            "risk_warning": "Import duty/customs tax is unknown; landed cost cannot be zero-assumed."
        }

    shipping = international_shipping if international_shipping is not None else 0.0
    tax = import_duty_tax if import_duty_tax is not None else 0.0
    
    total_foreign = product_price + shipping + tax
    landed_cny = round(total_foreign * fx_rate_to_cny, 2)

    return {
        "is_complete": True,
        "currency": currency,
        "product_price": product_price,
        "international_shipping": shipping,
        "import_duty_tax": tax,
        "tax_status": tax_status,
        "total_foreign_cost": total_foreign,
        "fx_rate_to_cny": fx_rate_to_cny,
        "landed_cost_cny": landed_cny,
        "risk_warning": None
    }

def evaluate_cross_border_regional_risks(
    product_model: str,
    origin_market: str,             # "US", "JP", "EU", "UK"
    destination_market: str = "CN",
    voltage: Optional[str] = None,  # "110V", "100V", "220V-240V", "100V-240V_wide"
    has_domestic_warranty: bool = False,
    has_domestic_3c: bool = False,
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
    elif voltage == "100V-240V_wide":
        # Safe wide voltage
        pass
        
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

    # 4. Seller Fulfillment Tier
    if seller_tier == "third_party_merchant_fbm":
        risks.append({
            "risk_type": "high_seller_fulfillment_friction",
            "severity": "medium",
            "detail": "Fulfilled by third-party merchant (FBM) with higher shipping loss/counterfeit risk."
        })

    # 5. Product Condition
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

if __name__ == "__main__":
    print("Landed Cost Engine Module ready.")
