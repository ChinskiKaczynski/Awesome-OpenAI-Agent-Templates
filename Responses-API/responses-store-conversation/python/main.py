"""
Responses API - Stateful Conversations
Multi-turn conversations with store=True and previous_response_id.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def main():
    """Demonstrate multi-turn conversation with automatic context."""
    
    # First message - start the conversation
    print("👤 User: Tell me a joke")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Tell me a joke",
        store=True,  # Persist response on OpenAI servers
    )
    
    print(f"🤖 Assistant: {response.output_text}\n")
    
    # Second message - chain with previous_response_id
    print("👤 User: Explain why it's funny")
    
    second_response = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=response.id,  # Chain to previous
        input=[{"role": "user", "content": "Explain why this is funny."}],
        store=True,
    )
    
    print(f"🤖 Assistant: {second_response.output_text}\n")
    
    # Third message - continue the chain
    print("👤 User: Give me another joke on a similar theme")
    
    third_response = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=second_response.id,
        input=[{"role": "user", "content": "Give me another joke on a similar theme."}],
        store=True,
    )
    
    print(f"🤖 Assistant: {third_response.output_text}")
    
    # Print conversation chain info
    print(f"\n📊 Conversation chain:")
    print(f"   Response 1 ID: {response.id}")
    print(f"   Response 2 ID: {second_response.id}")
    print(f"   Response 3 ID: {third_response.id}")


if __name__ == "__main__":
    main()
