"""
Code Interpreter Agent
Sandboxed Python code execution using the code_interpreter built-in tool.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def run_code_interpreter(query: str) -> str:
    """Execute code using the code interpreter sandbox."""
    print(f"🧮 Query: {query}")
    print("🔧 Running code interpreter...")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=query,
        tools=[
            {
                "type": "code_interpreter",
                "container": {"type": "auto"}
            }
        ]
    )
    
    # Check for code interpreter outputs
    for output in response.output:
        if hasattr(output, 'type') and output.type == "code_interpreter_call":
            print(f"\n💻 Code executed:\n{output.code[:200]}...")
    
    return response.output_text


def main():
    """Demonstrate code interpreter with various tasks."""
    
    tasks = [
        "Calculate the factorial of 20 and verify it's correct",
        "Generate a list of the first 15 prime numbers",
        "Calculate the compound interest for $1000 at 5% for 10 years",
    ]
    
    for task in tasks:
        answer = run_code_interpreter(task)
        print(f"🤖 Answer: {answer}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
