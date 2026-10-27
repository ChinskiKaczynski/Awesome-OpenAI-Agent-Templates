"""
Web Search Agent
Real-time internet search using the web_search built-in tool.
"""
import os
from urllib.parse import urlsplit
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def has_valid_citation(annotation) -> bool:
    """Accept only HTTP(S) URLs in source annotations, not just the type label."""
    if annotation.type != "url_citation":
        return False
    url = getattr(annotation, "url", None)
    if not isinstance(url, str) or any(char.isspace() for char in url):
        return False
    try:
        parsed = urlsplit(url)
        _ = parsed.port  # Reject invalid ports.
        return parsed.scheme in ("http", "https") and bool(parsed.hostname)
    except ValueError:
        return False


def search_web(query: str) -> tuple[str, list[str]]:
    """Search the web for current information, requiring cited results."""
    print(f"🔍 Query: {query}")
    print("🌐 Searching the web...")

    response = client.responses.create(
        model="gpt-6-luna",
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

    # Keep the source URLs supplied by the API, not links invented by the model.
    sources = []
    for item in response.output:
        if item.type != "message":
            continue
        for part in item.content:
            if part.type != "output_text":
                continue
            for annotation in part.annotations or []:
                if has_valid_citation(annotation) and annotation.url not in sources:
                    sources.append(annotation.url)
    if not sources:
        raise RuntimeError("Web search answer has no source citations.")
    return response.output_text, sources


def main():
    """Demonstrate web search with multiple queries."""
    queries = [
        "Who is the current president of France?",
        "What are the latest developments in AI?",
    ]
    for query in queries:
        answer, sources = search_web(query)
        print(f"🤖 Answer: {answer}\n")
        print("Sources:\n" + "\n".join(f"- {url}" for url in sources))
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
