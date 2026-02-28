import logging
import os

_CONFIGURED = False

def setup_logging():
    global _CONFIGURED
    if _CONFIGURED:
        return

    level = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Human note: keeping logs predictable matters more than fancy formatting in small teams.
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    _CONFIGURED = True
