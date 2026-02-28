import os
from llm.client import get_provider

def main():
    p = get_provider()
    prompt = os.getenv("LLM_DEMO_PROMPT", "Summarize: I shipped a runnable repo skeleton for Upwork.")
    r = p.generate(prompt)
    print(r.text)

if __name__ == "__main__":
    main()
