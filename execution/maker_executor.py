import asyncio
from typing import Dict, Any
from infra.api_client import ApiClient

class MakerExecutor:
    def __init__(self, api: ApiClient):
        self.api = api

    async def place_order(self, symbol: str, side: str, price: float, size: float) -> Dict[str, Any]:
        return await self.api.post("/order", {
            "symbol": symbol,
            "side": side,
            "price": price,
            "size": size
        })

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return await self.api.post("/cancel", {"order_id": order_id})

    async def re_quote(self, symbol: str):
        await asyncio.sleep(0.1)
        return {"status": "re-quoted"}
