"""
Web Search Agent
Real-time internet search using the web_search built-in tool.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def search_web(query: str) -> str:
    """Search the web for current information."""
    print(f"🔍 Query: {query}")
    print("🌐 Searching the web...")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=query,
        tools=[{"type": "web_search_preview"}]
    )
    
    return response.output_text


def main():
    """Demonstrate web search with multiple queries."""
    
    queries = [
        "Who is the current president of France?",
        "What are the latest developments in AI?",
    ]
    
    for query in queries:
        answer = search_web(query)
        print(f"🤖 Answer: {answer}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
