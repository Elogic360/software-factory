"""Kong Admin Gateway MCP Server (Read-only discovery)."""
import os
import httpx
from typing import Dict, Any

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://localhost:8001")

async def get_services() -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{KONG_ADMIN_URL}/services")
            return resp.json() if resp.status_code == 200 else {"services": []}
        except Exception as e:
            return {"error": str(e)}

async def get_routes() -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{KONG_ADMIN_URL}/routes")
            return resp.json() if resp.status_code == 200 else {"routes": []}
        except Exception as e:
            return {"error": str(e)}
