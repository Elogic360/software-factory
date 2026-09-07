"""Unified Market Data Normalizer MCP Server."""
from typing import Dict, Any

def normalize_ohlcv(raw_ticker: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "symbol": raw_ticker.get("symbol") or raw_ticker.get("s", "UNKNOWN"),
        "price": float(raw_ticker.get("price") or raw_ticker.get("c", 0.0)),
        "change_24h": float(raw_ticker.get("change") or raw_ticker.get("d", 0.0)),
        "percent_change": float(raw_ticker.get("change_percent") or raw_ticker.get("dp", 0.0)),
        "volume": float(raw_ticker.get("volume") or raw_ticker.get("v", 0.0)),
    }
