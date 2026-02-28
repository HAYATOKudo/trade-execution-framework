from __future__ import annotations

import asyncio
import json
import logging
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


log = logging.getLogger("infra.api_client")


@dataclass(frozen=True)
class ApiError(Exception):
    status: int
    message: str
    body: Optional[str] = None


class ApiClient:
    '''
    Public skeleton HTTP client.

    This intentionally uses stdlib only (no requests/httpx)
    to keep the public repo dependency-light.

    Real-world API pain points:
    - transient network failures
    - rate limits (429)
    - APIs returning 200 but containing business errors
    '''

    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)

    def _build(self, method: str, path: str, data: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json", "User-Agent": "trade-execution-framework/0.1"}
        payload = None
        if data is not None:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        return urllib.request.Request(url, data=payload, headers=headers, method=method)

    async def request_json(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        req = self._build(method, path, data)
        last_err: Optional[Exception] = None

        for attempt in range(self.max_retries):
            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    status = getattr(resp, "status", 200)
                    body = resp.read().decode("utf-8", errors="replace")

                    if status < 200 or status >= 300:
                        raise ApiError(status=status, message="HTTP error", body=body)

                    try:
                        obj = json.loads(body) if body else {}
                    except Exception:
                        raise ApiError(status=status, message="Invalid JSON", body=body)

                    dt = (time.time() - t0) * 1000.0
                    log.info("HTTP %s %s -> %s (%.1fms)", method, path, status, dt)

                    if not isinstance(obj, dict):
                        raise ApiError(status=status, message="JSON root not object", body=body)

                    return obj

            except urllib.error.HTTPError as e:
                status = getattr(e, "code", 0) or 0
                retryable = status in (429, 500, 502, 503, 504)
                last_err = e

                if not retryable or attempt == self.max_retries - 1:
                    raise

            except Exception as e:
                last_err = e
                if attempt == self.max_retries - 1:
                    raise

            backoff = min(2.0, 0.25 * (2 ** attempt))
            jitter = random.random() * 0.1
            await asyncio.sleep(backoff + jitter)

        assert last_err is not None
        raise last_err

    async def get(self, path: str) -> Dict[str, Any]:
        return await self.request_json("GET", path)

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.request_json("POST", path, data)
