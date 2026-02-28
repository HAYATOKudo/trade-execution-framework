import os, asyncio, json
from typing import Any, Dict, Optional
import urllib.request, urllib.error

class ApiClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def _request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        payload = None
        headers = {"Content-Type": "application/json"}
        if data:
            payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=headers, method=method)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode())
            except Exception as e:
                if attempt == 2:
                    raise
                await asyncio.sleep(0.5)

    async def get(self, path: str) -> Dict[str, Any]:
        return await self._request("GET", path)

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", path, data)
