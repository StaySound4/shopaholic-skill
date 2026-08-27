#!/usr/bin/env python3
"""Strict current, cross-sectional, and historical price semantics engine.
Attaches full identity, region, seller channel, observation date, currency,
and promotional conditions to every price claim. Distinguishes same-day cross-sectional
merchant spreads from multi-date time-series historical price trends, and enforces
condition transparency without stripping subsidies or coupons.
"""
from typing import Any, Dict, List, Optional
import datetime

class PriceObservation:
    def __init__(
        self,
        product_id: str,
        price_amount: float,
        currency: str = "CNY",
        region: str = "CN-Mainland",
        channel_seller: str = "JD_SelfOperated",
        observation_date: str = "2026-08-28",
        is_unconditional_cash: bool = True,
        conditions: Optional[List[str]] = None
    ):
        self.product_id = product_id
        self.price_amount = float(price_amount)
        self.currency = currency
        self.region = region
        self.channel_seller = channel_seller
        self.observation_date = observation_date
        self.is_unconditional_cash = is_unconditional_cash
        self.conditions = conditions or []
        
        # Validation: If conditions exist, cannot claim unconditional cash
        if self.conditions and self.is_unconditional_cash:
            raise ValueError(f"Price with conditions {self.conditions} cannot be marked as unconditional cash.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "price_amount": self.price_amount,
            "currency": self.currency,
            "region": self.region,
            "channel_seller": self.channel_seller,
            "observation_date": self.observation_date,
            "is_unconditional_cash": self.is_unconditional_cash,
            "conditions": self.conditions
        }

def analyze_price_observations(observations: List[PriceObservation]) -> Dict[str, Any]:
    """Analyzes price observations to classify cross-sectional spread vs historical range."""
    if not observations:
        raise ValueError("Cannot analyze empty price observations.")

    obs_dicts = [o.to_dict() for o in observations]
    dates = sorted(list(set(o["observation_date"] for o in obs_dicts)))
    channels = sorted(list(set(o["channel_seller"] for o in obs_dicts)))
    prices = [o["price_amount"] for o in obs_dicts]
    
    min_price = min(prices)
    max_price = max(prices)
    
    # 1. Check if all observations occurred on the same date across different sellers
    if len(dates) == 1:
        return {
            "analysis_type": "cross_sectional_spread",
            "observation_date": dates[0],
            "seller_count": len(channels),
            "channels": channels,
            "price_spread": {"min": min_price, "max": max_price, "spread": max_price - min_price},
            "is_historical_trend": False,
            "label": f"Same-day cross-sectional spread across {len(channels)} sellers on {dates[0]}"
        }

    # 2. Check if observations span multiple distinct dates -> Historical time-series
    start_d = datetime.date.fromisoformat(dates[0])
    end_d = datetime.date.fromisoformat(dates[-1])
    span_days = (end_d - start_d).days

    return {
        "analysis_type": "historical_time_series_range",
        "date_span_days": span_days,
        "earliest_date": dates[0],
        "latest_date": dates[-1],
        "observation_count": len(obs_dicts),
        "historical_range": {"min": min_price, "max": max_price},
        "is_historical_trend": True,
        "label": f"Historical {span_days}-day time-series range ({dates[0]} to {dates[-1]})"
    }

def format_price_display(obs: PriceObservation) -> str:
    """Formats price claim with mandatory conditional disclosures."""
    if obs.is_unconditional_cash:
        return f"{obs.currency} {obs.price_amount:.2f} (Direct Cash / No Conditions)"
    
    conds_str = ", ".join(obs.conditions)
    return f"{obs.currency} {obs.price_amount:.2f} [Conditional: {conds_str}]"

if __name__ == "__main__":
    print("Price Semantics Engine Module ready.")
