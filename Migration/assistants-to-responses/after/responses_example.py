"""
Responses API Example (AFTER Migration)
This code uses the recommended Responses API.
Migrated from the Assistants API example.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def run_conversation(user_message: str) -> str:
    """
    Run a conversation using the Responses API.
    
    Key differences from Assistants API:
    - No thread/run management
    - Single API call
    - Built-in code interpreter
    - No polling required
    """
    
    response = client.responses.create(
        model="gpt-4o-mini",
        # Instructions are passed directly (no assistant object)
        instructions="You are a helpful math tutor. Solve problems step by step.",
        input=user_message,
        # Tools are built-in
        tools=[
            {
                "type": "code_interpreter",
                "container": {"type": "auto"}
            }
        ],
        # Store for potential follow-up questions
        store=True
    )
    
    return response.output_text, response.id


def run_follow_up(previous_id: str, follow_up_message: str) -> str:
    """
    Follow-up question using previous_response_id.
    This replaces thread-based conversation management.
    """
    
    response = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=previous_id,  # Chain to previous
        input=[{"role": "user", "content": follow_up_message}],
        tools=[
            {
                "type": "code_interpreter",
                "container": {"type": "auto"}
            }
        ],
        store=True
    )
    
    return response.output_text, response.id


def main():
    print("✅ This uses the recommended Responses API")
    print("   No threads, no runs, no polling!\n")
    
    # First question - much simpler!
    print("👤 User: What is 25 factorial? Show your work.")
    response_text, response_id = run_conversation(
        "What is 25 factorial? Show your work."
    )
    print(f"🤖 Assistant: {response_text}\n")
    
    # Follow-up using previous_response_id (replaces thread)
    print("👤 User: Now divide that by 24 factorial")
    follow_up_text, _ = run_follow_up(
        response_id,
        "Now divide that by 24 factorial. What do you get?"
    )
    print(f"🤖 Assistant: {follow_up_text}")
    
    # No cleanup needed - no persistent assistant object


if __name__ == "__main__":
    main()
