import asyncio
import logging

from infra.api_client import ApiClient
from execution.maker_executor import MakerExecutor
from strategy.stub_strategy import decide_signal
from tools.logging_config import setup_logging
from app_config.settings import get_base_url, get_timeout_sec


log = logging.getLogger("live.run")


async def main():
    setup_logging()

    base_url = get_base_url()
    timeout = get_timeout_sec()
    log.info("starting demo base_url=%s timeout=%.2fs", base_url, timeout)

    api = ApiClient(base_url, timeout=timeout, max_retries=3)
    executor = MakerExecutor(api, replace_sec=1.0, max_requotes=3)

    # Connectivity smoke check
    try:
        ping = await api.get("/get")
        log.info("connectivity ok keys=%s", ",".join(list(ping.keys())[:5]))
    except Exception as e:
        log.error("connectivity failed: %s", e)
        raise

    signal = decide_signal({})
    print("Signal:", signal)

    if signal.action == "NO_TRADE":
        print("No trade executed.")
        return

    print("Trade routing is intentionally excluded from the public repo.")


if __name__ == "__main__":
    asyncio.run(main())
