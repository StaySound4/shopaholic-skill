#!/usr/bin/env python3
"""Official domestic and global source-routing playbooks (Wayfinding & Search Anchors).
Provides structured routing, query syntax anchors, proof roles, and access caveats
across 5 domains (Electrical/Safety, Energy/Ecology, Food/Baby/Health, Audio/Display/Interconnect,
Outdoor/Materials). Strictly avoids static text hoarding in favor of dynamic runtime verification.
"""
from typing import Any, Dict, List, Optional

SOURCE_ROUTING_PLAYBOOKS = {
    "electrical_safety": {
        "domain": "Electrical, Radio & Physical Safety",
        "authoritative_sources": [
            {
                "source_id": "CN_3C_CNCA",
                "name": "China Compulsory Certification (CNCA / CQC)",
                "portal_url": "http://cx.cnca.cn",
                "search_syntax_anchor": 'site:cqc.com.cn OR site:cnca.gov.cn "{model_or_certificate}"',
                "what_it_proves": "Mandatory China market electrical/safety compliance, factory locator, and certificate validity.",
                "cannot_prove_alone": "Performance metrics, acoustic quality, or long-term component durability beyond standard safety limits.",
                "access_caveat": "Requires captcha / rate-limited portal; fallback to manufacturer 3C declaration + CNAS test report check."
            },
            {
                "source_id": "US_FCC_ID",
                "name": "US FCC OET Equipment Authorization Database",
                "portal_url": "https://www.fcc.gov/oet/ea/fccid",
                "search_syntax_anchor": 'site:fcc.gov/oet/ea/fccid "{fcc_grantee_code}" OR "{fcc_product_code}"',
                "what_it_proves": "RF emissions compliance, internal PCB high-res teardown photos, Change in ID / OEM design identity.",
                "cannot_prove_alone": "Thermal heatsink or exterior cosmetic changes made for domestic region SKU variants.",
                "access_caveat": "Publicly accessible; grant confidentiality may withhold schematics."
            },
            {
                "source_id": "GLOBAL_UL_IQ",
                "name": "UL Product iQ",
                "portal_url": "https://productiq.ulprospector.com",
                "search_syntax_anchor": 'site:ul.com OR "UL Product iQ" "{model_number}"',
                "what_it_proves": "North American safety listing and UL component yellow-card flammability ratings.",
                "cannot_prove_alone": "Compliance with regional Chinese GB standards.",
                "access_caveat": "Requires free login; fallback to UL certificate PDF verification."
            }
        ]
    },
    "energy_ecology": {
        "domain": "Energy Efficiency & Eco-Design",
        "authoritative_sources": [
            {
                "source_id": "EU_EPREL",
                "name": "European Product Registry for Energy Labelling (EPREL)",
                "portal_url": "https://eprel.ec.europa.eu",
                "search_syntax_anchor": 'site:eprel.ec.europa.eu "{model_or_registration_number}"',
                "what_it_proves": "Standardized energy consumption logs, HDR luminance power draw, noise emission grades.",
                "cannot_prove_alone": "Domestic Chinese Tier 1/2 energy efficiency tier (must check CEL).",
                "access_caveat": "Open public EU API and web interface."
            },
            {
                "source_id": "CN_CEL",
                "name": "China Energy Label (中国能效标识网)",
                "portal_url": "http://www.energylabel.gov.cn",
                "search_syntax_anchor": 'site:energylabel.gov.cn "{model_number}"',
                "what_it_proves": "Domestic Chinese energy efficiency grade, standby power draw, and registered test laboratory.",
                "cannot_prove_alone": "Real-world peak dynamic load energy under extreme gaming/heavy compute scenarios.",
                "access_caveat": "Public search available."
            }
        ]
    },
    "food_baby_health": {
        "domain": "Food Contact, Baby & Medical Health",
        "authoritative_sources": [
            {
                "source_id": "CN_SAMR_STANDARDS",
                "name": "National Standard Public Service Platform (国家标准信息服务平台)",
                "portal_url": "https://std.samr.gov.cn",
                "search_syntax_anchor": 'site:std.samr.gov.cn "{standard_code}"',
                "what_it_proves": "Authoritative active, upcoming, or superseded temporal status of GB/T and GB mandatory standards.",
                "cannot_prove_alone": "Whether a specific SKU batch actually complies with the standard without CNAS lab test report.",
                "access_caveat": "Open public access."
            },
            {
                "source_id": "UN_ECE_R129",
                "name": "UN ECE R129 / i-Size Child Restraint Approval Registry",
                "portal_url": "https://unece.org/transport/vehicle-regulations",
                "search_syntax_anchor": '"ECE R129" OR "i-Size" "{approval_number}"',
                "what_it_proves": "Side-impact dynamic crash testing and Q-dummy sensor injury criteria compliance.",
                "cannot_prove_alone": "Fabric flame retardancy under domestic GB standards without separate 3C test.",
                "access_caveat": "Approval labels physically visible on child car seat shell."
            }
        ]
    },
    "audio_display_interconnect": {
        "domain": "Audio, Display, Video & Protocols",
        "authoritative_sources": [
            {
                "source_id": "VESA_DISPLAYHDR",
                "name": "VESA Certified DisplayHDR Database",
                "portal_url": "https://displayhdr.org/certified-products",
                "search_syntax_anchor": 'site:displayhdr.org/certified-products "{model_name}"',
                "what_it_proves": "True certified HDR peak luminance, full-screen sustained brightness, contrast ratio, and color gamut.",
                "cannot_prove_alone": "Motion clarity (pixel response time GtG) or backlight PWM flicker frequency.",
                "access_caveat": "Publicly searchable database."
            },
            {
                "source_id": "USB_IF_INTEGRATORS",
                "name": "USB-IF Certified Integrators List",
                "portal_url": "https://www.usb.org/products",
                "search_syntax_anchor": 'site:usb.org/products "{test_id_or_model}"',
                "what_it_proves": "Official USB-IF silicon/cable TID compliance with USB Power Delivery specifications.",
                "cannot_prove_alone": "Physical noncompliance of unlisted products (voluntary membership listing).",
                "access_caveat": "Voluntary registry: absence indicates unverified listing, NOT counterfeit or illegal."
            }
        ]
    },
    "outdoor_materials": {
        "domain": "Outdoor Gear, Durability & Ethical Materials",
        "authoritative_sources": [
            {
                "source_id": "UIAA_SAFETY",
                "name": "UIAA Climbing and Mountaineering Safety Standards Registry",
                "portal_url": "https://theuiaa.org/safety-standards/certified-equipment",
                "search_syntax_anchor": 'site:theuiaa.org/safety-standards/certified-equipment "{model_or_brand}"',
                "what_it_proves": "Dynamic fall impact force ratings, sharp edge cut resistance, and carabiner gate breaking strength.",
                "cannot_prove_alone": "Long-term UV degradation after years of uncontrolled storage.",
                "access_caveat": "Public global database."
            }
        ]
    }
}

def route_claim_to_source_playbook(claim_type: str, query_variable: str) -> Dict[str, Any]:
    """Finds matching authoritative portal playbook and generates runtime query syntax."""
    claim_type_lower = claim_type.lower()
    
    # Check domain routing
    if "hdr" in claim_type_lower or "vesa" in claim_type_lower:
        domain_key = "audio_display_interconnect"
        src_id = "VESA_DISPLAYHDR"
    elif "usb" in claim_type_lower or "power_delivery" in claim_type_lower:
        domain_key = "audio_display_interconnect"
        src_id = "USB_IF_INTEGRATORS"
    elif "standard" in claim_type_lower or "gb" in claim_type_lower or "food" in claim_type_lower:
        domain_key = "food_baby_health"
        src_id = "CN_SAMR_STANDARDS"
    elif "fcc" in claim_type_lower or "rf" in claim_type_lower or "teardown" in claim_type_lower:
        domain_key = "electrical_safety"
        src_id = "US_FCC_ID"
    elif "eprel" in claim_type_lower or "energy" in claim_type_lower:
        domain_key = "energy_ecology"
        src_id = "EU_EPREL"
    else:
        domain_key = "electrical_safety"
        src_id = "CN_3C_CNCA"

    domain_pb = SOURCE_ROUTING_PLAYBOOKS[domain_key]
    source_entry = [s for s in domain_pb["authoritative_sources"] if s["source_id"] == src_id][0]
    
    # Format search syntax
    formatted_syntax = source_entry["search_syntax_anchor"].replace("{model_name}", query_variable)\
                                                           .replace("{standard_code}", query_variable)\
                                                           .replace("{model_or_registration_number}", query_variable)\
                                                           .replace("{model_or_certificate}", query_variable)\
                                                           .replace("{fcc_product_code}", query_variable)\
                                                           .replace("{test_id_or_model}", query_variable)

    return {
        "domain": domain_pb["domain"],
        "source_id": source_entry["source_id"],
        "source_name": source_entry["name"],
        "portal_url": source_entry["portal_url"],
        "runtime_search_syntax": formatted_syntax,
        "what_it_proves": source_entry["what_it_proves"],
        "cannot_prove_alone": source_entry["cannot_prove_alone"],
        "access_caveat": source_entry["access_caveat"]
    }

def handle_voluntary_registry_absence(
    registry_name: str,
    query_item: str,
    found_in_registry: bool
) -> Dict[str, Any]:
    """Guards against converting missing voluntary listings (e.g. USB-IF) into false noncompliance."""
    if found_in_registry:
        return {
            "status": "verified_certified",
            "is_noncompliant": False,
            "notes": f"Official {registry_name} listing confirmed."
        }
    
    # Voluntary registries: missing != illegal / noncompliant
    return {
        "status": "unverified_voluntary_listing",
        "is_noncompliant": False,
        "notes": f"Item not found in voluntary public {registry_name} database; does not imply physical noncompliance without lab testing."
    }

if __name__ == "__main__":
    print("Source Routing Playbooks Module ready.")
