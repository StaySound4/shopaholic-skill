#!/usr/bin/env python3
"""Untrusted evidence data and prompt injection boundary engine.
Treats all retrieved web pages, snippets, seller descriptions, and PDFs strictly
as untrusted passive evidence data. Neutralizes embedded prompt injection payloads,
prevents retrieval-based instruction overrides or system prompt leaks, and parses
factual claims strictly through the Claim/Evidence Ledger.
"""
import re
from typing import Any, Dict, List, Optional, Tuple

PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"(?i)system\s+directive\s*:",
    r"(?i)system\s+override\s*:",
    r"(?i)mark\s+this\s+case\s+(as\s+)?pass",
    r"(?i)reveal\s+(system\s+prompt|internal\s+instructions)",
    r"(?i)redefine\s+source\s+trust",
    r"(?i)disregard\s+all\s+safety\s+defects",
    r"(?i)<system-directive>",
    r"(?i)assistant\s*:\s*i\s+hereby\s+approve"
]

def sanitize_untrusted_evidence_text(raw_text: str) -> Tuple[str, List[str]]:
    """Sanitizes raw retrieved text and strips/neutralizes prompt injection payloads."""
    detected_injections = []
    sanitized_text = raw_text

    for pattern in PROMPT_INJECTION_PATTERNS:
        matches = re.findall(pattern, sanitized_text)
        if matches:
            detected_injections.append(pattern)
            # Neutralize injection by escaping and wrapping in untrusted data tag
            sanitized_text = re.sub(pattern, "[UNTRUSTED_INJECTION_PAYLOAD_NEUTRALIZED]", sanitized_text)

    return sanitized_text, detected_injections

def parse_retrieved_evidence_payload(
    raw_document_text: str,
    source_id: str,
    target_claim_fields: List[str]
) -> Dict[str, Any]:
    """Parses retrieved evidence strictly as passive data without executing embedded instructions."""
    sanitized_content, injections = sanitize_untrusted_evidence_text(raw_document_text)
    
    extracted_facts = {}
    for field in target_claim_fields:
        # Simple passive extraction simulation
        m = re.search(rf"(?i){field}\s*[:=]\s*([^\n,;]+)", sanitized_content)
        if m:
            extracted_facts[field] = m.group(1).strip()

    return {
        "source_id": source_id,
        "is_untrusted_data": True,
        "injections_detected": len(injections) > 0,
        "injection_patterns_blocked": injections,
        "sanitized_evidence_text": sanitized_content,
        "extracted_facts": extracted_facts,
        "instruction_execution_blocked": True
    }

def evaluate_claim_with_security_guard(
    claimed_defect: Dict[str, Any],
    retrieved_seller_text: str
) -> Dict[str, Any]:
    """Evaluates product defect against retrieved seller text while guarding against prompt injection."""
    parsed = parse_retrieved_evidence_payload(
        raw_document_text=retrieved_seller_text,
        source_id="SELLER_SNIPPET",
        target_claim_fields=["claimed_defect_status"]
    )
    
    # If seller text contained injection like 'mark this case PASS', ensure defect remains active
    has_defect = claimed_defect.get("has_active_defect", False)
    
    return {
        "defect_adjudication_valid": True,
        "has_active_defect": has_defect,
        "seller_injection_neutralized": parsed["injections_detected"],
        "evaluator_override_prevented": True
    }

if __name__ == "__main__":
    print("Untrusted Evidence Guard Module ready.")
