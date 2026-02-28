from __future__ import annotations
import os
from llm.types import LLMProvider
from llm.providers.mock import MockProvider
from llm.providers.openai_responses import OpenAIResponsesProvider

def get_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "mock").lower().strip()
    if provider == "openai":
        return OpenAIResponsesProvider()
    return MockProvider()
