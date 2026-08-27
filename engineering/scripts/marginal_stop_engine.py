#!/usr/bin/env python3
"""Marginal information stop rule and dynamic candidate count engine.
Replaces fixed candidate quotas (3+2+1, 10-15 search quotas) with an information-gain
convergence model that stops when decision-relevant marginal gain ceases and outputs
0, 1, 2, 3, or more strictly justified candidates without artificial padding.
"""
import json, sys
from typing import Any, List, Dict, Optional

# Recognized information-gain signal types
INFORMATION_GAIN_TYPES = {
    "new_technology_route",      # Distinct technical architecture / principle
    "identity_correction",       # Real OEM, unmasked rebadge, revision fix
    "safety_signal_finding",     # Recall, toxicological risk, structural defect
    "pareto_frontier_candidate", # Dominates or establishes new non-dominated trade-off
    "value_frontier_entry"       # Unprecedented cost-to-performance frontier
}

class DiscoverySession:
    def __init__(self, category: str, research_budget: str = "R1"):
        self.category = category
        self.research_budget = research_budget
        self.passes: List[Dict[str, Any]] = []
        self.consecutive_no_gain_passes: int = 0
        self.unresolved_critical_claims: int = 0
        self.discovered_candidates: List[Dict[str, Any]] = []
        self.stopped: bool = False
        self.stop_reason: Optional[str] = None

    def record_pass(
        self,
        query: str,
        information_gains: List[Dict[str, str]],
        unresolved_critical_claims: int = 0,
        new_candidates: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Records a search/discovery pass and checks stopping criteria."""
        if self.stopped:
            return {"stopped": True, "reason": self.stop_reason}

        self.unresolved_critical_claims = unresolved_critical_claims
        valid_gains = [g for g in information_gains if g.get("gain_type") in INFORMATION_GAIN_TYPES]
        
        has_gain = len(valid_gains) > 0
        if has_gain:
            self.consecutive_no_gain_passes = 0
        else:
            self.consecutive_no_gain_passes += 1

        if new_candidates:
            for cand in new_candidates:
                if cand not in self.discovered_candidates:
                    self.discovered_candidates.append(cand)

        pass_record = {
            "pass_index": len(self.passes) + 1,
            "query": query,
            "gain_count": len(valid_gains),
            "gains": valid_gains,
            "consecutive_no_gain_passes": self.consecutive_no_gain_passes,
            "unresolved_critical_claims": self.unresolved_critical_claims
        }
        self.passes.append(pass_record)

        # Check stop conditions
        # 1. 2 consecutive passes with zero decision-relevant gain AND no unresolved critical claims
        if self.consecutive_no_gain_passes >= 2 and self.unresolved_critical_claims == 0:
            self.stopped = True
            self.stop_reason = "Marginal information gain exhausted: 2 consecutive no-gain passes with 0 unresolved critical claims."
            
        return {
            "stopped": self.stopped,
            "stop_reason": self.stop_reason,
            "current_pass": pass_record,
            "candidate_count": len(self.discovered_candidates)
        }

    def finalize_candidates(self, viable_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Finalizes recommendations without artificial padding or quota forcing."""
        # Never artificially pad to meet a minimum (e.g., forcing 3 candidates when only 1 is viable)
        return {
            "candidate_count": len(viable_candidates),
            "candidates": viable_candidates,
            "padding_applied": False,
            "stop_reason": self.stop_reason or "Convergence reached",
            "total_passes": len(self.passes)
        }

if __name__ == "__main__":
    print("Marginal Stop Engine Module ready.")
