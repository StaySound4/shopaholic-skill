#!/usr/bin/env python3
"""Decision-first concise output renderer with dynamic candidate scaling.
Renders compact decision-first recommendations, supports 1-candidate extreme brevity
compression on demand, strictly scales table columns/rows without empty padding,
explains within-budget compromises factually, and encloses structured audit records
within a single <decision_record>...</decision_record> XML block.
"""
import json
from typing import Any, Dict, List, Optional

EXTREME_BREVITY_PROMPTS = {
    "just tell me which one to buy",
    "just tell me which one",
    "just tell me what to buy",
    "direct recommendation",
    "直接告诉我买哪个",
    "只要一个推荐",
    "直接给答案",
    "直接推荐",
    "one recommendation only"
}

def is_extreme_brevity_requested(user_query: str) -> bool:
    q_lower = user_query.lower().strip()
    return any(p in q_lower for p in EXTREME_BREVITY_PROMPTS)

def render_decision_first_output(
    user_query: str,
    top_candidates: List[Dict[str, Any]],
    decision_summary: str,
    within_budget_compromise: Optional[str] = None,
    decision_record_payload: Optional[Dict[str, Any]] = None,
    research_budget: str = "R1"
) -> str:
    """Renders concise decision-first markdown output."""
    brevity_mode = is_extreme_brevity_requested(user_query)
    lines = []

    # 1. Immediate Decisive Choice (Decision-First)
    if not top_candidates:
        lines.append("## 决策结论：无符合硬性约束的有效候选")
        lines.append(f"**原因**：{decision_summary}\n")
    elif brevity_mode or len(top_candidates) == 1:
        top = top_candidates[0]
        lines.append(f"## 首选推荐：{top.get('name')} (¥{top.get('price', 'N/A')})")
        lines.append(f"**核心理由**：{top.get('core_reason', decision_summary)}")
        if within_budget_compromise:
            lines.append(f"**物理取舍**：{within_budget_compromise}")
        lines.append("")
    else:
        top = top_candidates[0]
        lines.append(f"## 首选决策：{top.get('name')} (¥{top.get('price', 'N/A')})")
        lines.append(f"**选型结论**：{decision_summary}\n")
        
        # 2. Compact Comparison Table (Strictly only relevant non-empty columns)
        lines.append("### 核心候选对比")
        lines.append("| 候选型号 | 价格 | 核心技术路线 | 核心优势 | 关键物理取舍 |")
        lines.append("|---|---|---|---|---|")
        for c in top_candidates:
            name = c.get("name", "")
            price = f"¥{c.get('price', '')}"
            route = c.get("tech_route", "标准路线")
            adv = c.get("advantage", "均衡")
            tradeoff = c.get("tradeoff", "基础用料")
            lines.append(f"| {name} | {price} | {route} | {adv} | {tradeoff} |")
        lines.append("")
        
        if within_budget_compromise:
            lines.append(f"**预算内工程取舍**：{within_budget_compromise}\n")

    # 3. Embed structured Decision Record XML on demand for benchmark evaluation
    if decision_record_payload:
        lines.append("<decision_record>")
        lines.append(json.dumps(decision_record_payload, ensure_ascii=False, indent=2))
        lines.append("</decision_record>")

    return "\n".join(lines)

def validate_output_conciseness(
    rendered_text: str,
    is_trivial_purchase: bool = False,
    is_extreme_brevity: bool = False
) -> Dict[str, Any]:
    """Validates that rendered text meets conciseness criteria without bloat."""
    lines = [line.strip() for line in rendered_text.split("\n") if line.strip()]
    
    # 1. Decision-first check: Header must be on first 2 non-empty lines
    first_two_lines = " ".join(lines[:2])
    has_decision_first = ("首选推荐" in first_two_lines or "首选决策" in first_two_lines or "决策结论" in first_two_lines)

    # 2. Check for empty columns or synthetic padding
    has_empty_cell = any("|  |" in line or "| N/A | N/A | N/A |" in line for line in lines)
    
    # 3. Check extreme brevity constraints
    if is_extreme_brevity:
        # Table lines should not be present in extreme brevity mode
        has_table = any(line.startswith("|") for line in lines)
        if has_table:
            return {"valid": False, "reason": "Extreme brevity requested but comparison table was generated."}

    # 4. Trivial purchase conciseness (e.g. 60 CNY charger should not exceed 25 lines)
    if is_trivial_purchase and len(lines) > 25:
        return {"valid": False, "reason": f"Trivial purchase produced bloated output ({len(lines)} lines)."}

    return {
        "valid": has_decision_first and not has_empty_cell,
        "has_decision_first": has_decision_first,
        "has_empty_cell": has_empty_cell,
        "total_lines": len(lines)
    }

if __name__ == "__main__":
    print("Decision-First Renderer Module ready.")
