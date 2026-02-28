from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any

Side = Literal["buy", "sell"]
PosSide = Literal["long", "short"]
Action = Literal["NO_TRADE","ENTER_LONG","EXIT_LONG","ENTER_SHORT","EXIT_SHORT"]

@dataclass(frozen=True)
class Signal:
    action: Action
    reason: str = ""
    meta: Optional[Dict[str, Any]] = None
