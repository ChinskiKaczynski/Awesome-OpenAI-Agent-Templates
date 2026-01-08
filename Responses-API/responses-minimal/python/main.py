"""
Responses API - Minimal Starter
The simplest possible example using OpenAI's Responses API.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def main():
    """Simple one-shot response request."""
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Hello! Tell me about yourself in one sentence.",
    )
    
    print(f"🤖 Response: {response.output_text}")
    print(f"📊 Usage: {response.usage.total_tokens} tokens")


if __name__ == "__main__":
    main()
