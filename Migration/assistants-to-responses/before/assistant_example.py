"""
Assistants API Example (BEFORE Migration)
This code uses the deprecated Assistants API.
Deadline for migration: August 26, 2026

WARNING: This is for reference only. Use the Responses API for new projects.
"""
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def create_assistant():
    """Create an assistant with code interpreter."""
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a helpful math tutor. Solve problems step by step.",
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}]
    )
    return assistant


def run_conversation(assistant_id: str, user_message: str):
    """Run a conversation using threads and runs."""
    
    # 1. Create a thread
    thread = client.beta.threads.create()
    print(f"Created thread: {thread.id}")
    
    # 2. Add user message to thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    
    # 3. Create a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    print(f"Created run: {run.id}")
    
    # 4. Poll until complete (the painful part)
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {run.status}")
    
    # 5. Get messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Return assistant's response
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value
    
    return None


def main():
    print("⚠️  WARNING: This uses the deprecated Assistants API")
    print("   Deadline: August 26, 2026")
    print("   See 'after/' folder for the Responses API version\n")
    
    # Create assistant
    assistant = create_assistant()
    print(f"Created assistant: {assistant.id}\n")
    
    # Run conversation
    response = run_conversation(
        assistant.id,
        "What is 25 factorial? Show your work."
    )
    
    print(f"\n🤖 Assistant: {response}")
    
    # Cleanup
    client.beta.assistants.delete(assistant.id)
    print("\n🧹 Cleaned up assistant")


if __name__ == "__main__":
    main()
