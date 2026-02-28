from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional, Dict, Any

@dataclass(frozen=True)
class LLMResult:
    text: str
    raw: Optional[Dict[str, Any]] = None

class LLMProvider(Protocol):
    def generate(self, prompt: str) -> LLMResult: ...
