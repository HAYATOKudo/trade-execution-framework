from __future__ import annotations
from llm.types import LLMResult

class MockProvider:
    def generate(self, prompt: str) -> LLMResult:
        return LLMResult(text=f"[MOCK] {prompt}")
