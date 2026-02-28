from __future__ import annotations
import os
from typing import Any, Dict, Optional
from llm.types import LLMResult

class OpenAIResponsesProvider:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()

    def generate(self, prompt: str) -> LLMResult:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Set it in .env (never commit .env).")

        try:
            from openai import OpenAI  # type: ignore
        except Exception as e:
            raise RuntimeError("openai package not installed. Run: pip install openai") from e

        client = OpenAI(api_key=self.api_key)
        resp = client.responses.create(
            model=self.model,
            input=prompt,
        )

        text = _extract_text(resp)
        raw: Optional[Dict[str, Any]] = None
        try:
            raw = resp.model_dump()  # type: ignore
        except Exception:
            raw = None
        return LLMResult(text=text, raw=raw)

def _extract_text(resp: Any) -> str:
    if hasattr(resp, "output_text") and isinstance(resp.output_text, str) and resp.output_text.strip():
        return resp.output_text.strip()

    try:
        d = resp.model_dump()
        out = d.get("output", [])
        parts = []
        for item in out:
            for c in item.get("content", []) or []:
                if c.get("type") == "output_text":
                    parts.append(c.get("text", ""))
        s = "".join(parts).strip()
        if s:
            return s
    except Exception:
        pass

    return str(resp)
