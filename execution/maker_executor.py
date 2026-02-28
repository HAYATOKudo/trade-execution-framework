from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from infra.api_client import ApiClient


log = logging.getLogger("execution.maker_executor")


@dataclass
class OrderState:
    '''
    Minimal state container used in execution loops.

    Real-world notes:
    - Partial fills happen.
    - Order acknowledgements may be delayed.
    - Requotes must be capped to avoid runaway fees.
    '''
    order_id: Optional[str] = None
    last_price: Optional[float] = None
    last_side: Optional[str] = None
    last_size: Optional[float] = None
    requote_count: int = 0


class MakerExecutor:
    '''
    Public skeleton maker executor.

    This demonstrates the structure of:
    quote -> place -> optional cancel/replace loop.

    Strategy logic is intentionally excluded.
    '''

    def __init__(self, api: ApiClient, *, replace_sec: float = 2.0, max_requotes: int = 20):
        self.api = api
        self.replace_sec = float(replace_sec)
        self.max_requotes = int(max_requotes)
        self.state = OrderState()

    @staticmethod
    def _normalize_price(price: float, tick: float = 0.5) -> float:
        # In production this depends on exchange metadata.
        return round(price / tick) * tick

    async def place_order(self, symbol: str, side: str, price: float, size: float) -> Dict[str, Any]:
        price_n = self._normalize_price(float(price))
        payload = {
            "symbol": symbol,
            "side": side,
            "price": price_n,
            "size": float(size),
            "post_only": True,
        }

        resp = await self.api.post("/order", payload)

        self.state.order_id = str(resp.get("order_id") or resp.get("id") or "")
        self.state.last_price = price_n
        self.state.last_side = side
        self.state.last_size = float(size)

        log.info(
            "placed order symbol=%s side=%s price=%.4f size=%.6f id=%s",
            symbol,
            side,
            price_n,
            float(size),
            self.state.order_id,
        )

        return resp

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        resp = await self.api.post("/cancel", {"order_id": order_id})
        log.info("canceled order id=%s", order_id)
        return resp

    async def cancel_if_exists(self) -> None:
        oid = (self.state.order_id or "").strip()
        if not oid:
            return
        try:
            await self.cancel_order(oid)
        finally:
            self.state.order_id = None

    async def requote_loop(self, symbol: str, side: str, price: float, size: float) -> Dict[str, Any]:
        '''
        Very small demo loop with hard cap on requotes.
        '''
        await self.cancel_if_exists()

        last: Dict[str, Any] = {}
        for i in range(self.max_requotes):
            self.state.requote_count = i + 1
            last = await self.place_order(symbol, side, price, size)

            # In real systems you would re-evaluate orderbook here.
            await asyncio.sleep(self.replace_sec)

        log.warning("requote_loop reached max_requotes=%s symbol=%s", self.max_requotes, symbol)
        return last
