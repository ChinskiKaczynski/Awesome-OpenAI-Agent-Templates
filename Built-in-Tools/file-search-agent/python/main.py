"""
File Search Agent
Document search using the file_search built-in tool with vector stores.

Prerequisites:
1. Create a vector store in OpenAI Dashboard
2. Upload documents to the vector store
3. Set VECTOR_STORE_ID environment variable
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Get vector store ID from environment or replace with your ID
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID", "vs_YOUR_VECTOR_STORE_ID")


def search_documents(query: str) -> str:
    """Search documents in the vector store."""
    print(f"📚 Query: {query}")
    print(f"🔍 Searching vector store {VECTOR_STORE_ID[:20]}...")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=query,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID]
            }
        ]
    )
    
    return response.output_text


def main():
    """Demonstrate file search with sample queries."""
    
    if VECTOR_STORE_ID == "vs_YOUR_VECTOR_STORE_ID":
        print("⚠️  Please set VECTOR_STORE_ID environment variable")
        print("   Create a vector store at: https://platform.openai.com/storage")
        return
    
    queries = [
        "What are the main topics covered in the documents?",
        "Summarize the key points from the documentation.",
    ]
    
    for query in queries:
        answer = search_documents(query)
        print(f"🤖 Answer: {answer}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
