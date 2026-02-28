from llm.client import get_provider

def summarize_ticket(text: str) -> str:
    p = get_provider()
    prompt = f""Summarize this customer message in 1 sentence and propose next action:\n\n{text}""
    return p.generate(prompt).text

if __name__ == ""__main__"":
    print(summarize_ticket(""Customer: I can't login after password reset.""))
