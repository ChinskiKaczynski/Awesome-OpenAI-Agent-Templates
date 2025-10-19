import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI  # noqa: E402

SYSTEM = "You are a helpful agent. Keep answers concise."

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Brak OPENAI_API_KEY. Ustaw w .env lub środowisku.")
        return
    client = OpenAI(api_key=api_key)
    print("Agent ready. Type 'quit' to exit.")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user},
            ],
        )
        print("Agent:", resp.choices[0].message.content)

if __name__ == "__main__":
    main()
