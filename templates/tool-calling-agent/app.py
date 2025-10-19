import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI  # noqa: E402
from tools.calculator import add  # noqa: E402
from tools.web_search import search  # noqa: E402

SYSTEM = "You are a helpful agent. Use tools when helpful. Keep answers brief."

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator_add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Return quick stubbed web results for a query.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

def call_tool(name, arguments):
    if name == "calculator_add":
        return {"result": add(arguments["a"], arguments["b"])}
    if name == "web_search":
        return {"results": search(arguments["query"])}
    return {"error": f"Unknown tool: {name}"}

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Brak OPENAI_API_KEY. Ustaw w .env lub środowisku.")
        return
    client = OpenAI(api_key=api_key)
    print("Tool-Calling Agent ready. Type 'quit' to exit.")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        msg = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
        first = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=msg,
            tools=TOOLS,
            tool_choice="auto",
        )
        choice = first.choices[0]
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            # Iterate tool calls
            for tc in choice.message.tool_calls:
                name = tc.function.name
                import json
                args = json.loads(tc.function.arguments or "{}")
                tool_output = call_tool(name, args)
                msg.append(choice.message)
                msg.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(tool_output)})
            # Final response
            final = client.chat.completions.create(model="gpt-4.1-mini", messages=msg)
            print("Agent:", final.choices[0].message.content)
        else:
            print("Agent:", choice.message.content)

if __name__ == "__main__":
    main()
