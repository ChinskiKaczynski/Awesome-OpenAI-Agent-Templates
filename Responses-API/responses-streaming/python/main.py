"""
Responses API - Streaming
Real-time streaming responses using Server-Sent Events (SSE).
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def main():
    """Stream response in real-time."""
    print("🔄 Streaming response...\n")
    
    stream = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": "Explain quantum entanglement in simple terms.",
            }
        ],
        stream=True,
    )
    
    # Iterate over streaming events
    for event in stream:
        # Handle text delta events
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        
        # Handle completion
        elif event.type == "response.completed":
            print(f"\n\n✅ Complete! Total tokens: {event.response.usage.total_tokens}")


if __name__ == "__main__":
    main()
