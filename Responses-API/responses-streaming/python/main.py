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
            usage = event.response.usage
            if usage is None:
                print("\n\n✅ Complete! Token usage unavailable.")
            else:
                print(f"\n\n✅ Complete! Total tokens: {usage.total_tokens}")

        elif event.type == "response.failed":
            error = event.response.error
            raise RuntimeError(f"Response failed: {error.message if error else 'Unknown error'}")

        elif event.type == "response.incomplete":
            details = event.response.incomplete_details
            raise RuntimeError(f"Response incomplete: {details.reason if details else 'Unknown reason'}")


if __name__ == "__main__":
    main()
