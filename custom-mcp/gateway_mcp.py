"""
Integral Market Custom FastMCP Gateway Servers
Exposes Finnhub, AlphaVantage, YahooFinance, Kong Admin API, and MT5 Bridge read-only MCP tools.
"""

from mcp.server.fastmcp import FastMCP
import os
import httpx

mcp = FastMCP("integral-market-custom-gateway")

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://localhost:8001")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

@mcp.tool()
async def kong_list_routes() -> str:
    """List all configured routes in Kong API Gateway."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{KONG_ADMIN_URL}/routes", timeout=5.0)
            return res.text
        except Exception as e:
            return f"Error contacting Kong Admin API: {str(e)}"

@mcp.tool()
async def kong_list_services() -> str:
    """List all registered services in Kong API Gateway."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{KONG_ADMIN_URL}/services", timeout=5.0)
            return res.text
        except Exception as e:
            return f"Error contacting Kong Admin API: {str(e)}"

@mcp.tool()
async def finnhub_quote(symbol: str) -> str:
    """Get real-time stock quote from Finnhub."""
    if not FINNHUB_API_KEY:
        return "FINNHUB_API_KEY not configured."
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}", timeout=5.0)
            return res.text
        except Exception as e:
            return f"Error fetching Finnhub quote: {str(e)}"

@mcp.tool()
async def alphavantage_fx_rate(from_currency: str, to_currency: str) -> str:
    """Get real-time exchange rate from Alpha Vantage."""
    if not ALPHA_VANTAGE_API_KEY:
        return "ALPHA_VANTAGE_API_KEY not configured."
    async with httpx.AsyncClient() as client:
        try:
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHA_VANTAGE_API_KEY}"
            res = await client.get(url, timeout=5.0)
            return res.text
        except Exception as e:
            return f"Error fetching AlphaVantage exchange rate: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
