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
    """Search the web for current information, requiring cited results."""
    print(f"🔍 Query: {query}")
    print("🌐 Searching the web...")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=query,
        tools=[{"type": "web_search"}],
        tool_choice="required",
    )

    # A required tool call is not proof that a search actually succeeded.
    calls = [item for item in response.output if item.type == "web_search_call"]
    if (
        response.status != "completed"
        or not calls
        or any(call.status != "completed" for call in calls)
    ):
        raise RuntimeError("Web search did not complete; no answer will be shown.")
    if not response.output_text or not response.output_text.strip():
        raise RuntimeError("Web search returned an empty answer.")

    cited = any(
        annotation.type == "url_citation"
        for item in response.output if item.type == "message"
        for part in item.content if part.type == "output_text"
        for annotation in part.annotations
    )
    if not cited:
        raise RuntimeError("Web search answer has no source citations.")
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
