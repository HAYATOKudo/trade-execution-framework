import asyncio
from infra.api_client import ApiClient
from execution.maker_executor import MakerExecutor
from strategy.stub_strategy import decide_signal
from tools.logging_config import setup_logging

async def main():
    setup_logging()
    api = ApiClient("https://httpbin.org")
    executor = MakerExecutor(api)

    signal = decide_signal({})
    print("Signal:", signal)

    if signal.action == "NO_TRADE":
        print("No trade executed.")
    else:
        print("Would execute trade here.")

if __name__ == "__main__":
    asyncio.run(main())
