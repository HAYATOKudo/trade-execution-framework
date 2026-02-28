import os


def get_base_url() -> str:
    return os.getenv("BASE_URL", "https://httpbin.org")


def get_timeout_sec() -> float:
    return float(os.getenv("TIMEOUT_SEC", "5"))
