"""Finnhub Market Intelligence MCP Server (Read-only)."""
import os
import httpx
from typing import Dict, Any

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

async def get_quote(symbol: str) -> Dict[str, Any]:
    if not FINNHUB_API_KEY:
        return {"error": "FINNHUB_API_KEY not set"}
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}")
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
