# Tool-Calling Agent (Python, Agents SDK)

**Goal:** Agent that can call **function tools** and **hosted tools** (Web Search, File Search).

## Setup
```bash
pip install openai-agents openai python-dotenv
export OPENAI_API_KEY=sk-...
```

## Configuration
- (Optional) Set `VECTOR_STORE_ID` if you have an OpenAI Vector Store with indexed files.

## Sample implementation
```python
# tool_agent.py
import os
from typing_extensions import TypedDict, Any
from agents import Agent, Runner, WebSearchTool, FileSearchTool, function_tool, RunContextWrapper

# Function tool with schema from annotations/docstring
class WeatherQuery(TypedDict):
    city: str
    unit: str  # "celsius" or "fahrenheit"

@function_tool
def get_weather(q: WeatherQuery) -> str:
    """Return a fake weather snapshot for demo.
    Args:
      q: { city, unit }
    """
    # Replace with real API integration as needed
    temp_c = 20
    if q["unit"] == "fahrenheit":
        temp_f = temp_c * 9/5 + 32
        return f"{q['city']}: {temp_f:.1f} °F, clear"
    return f"{q['city']}: {temp_c} °C, clear"

tools = [
    WebSearchTool(),
    # Limit file search to your vector store(s) if available
    FileSearchTool(max_num_results=3, vector_store_ids=[os.getenv("VECTOR_STORE_ID")] if os.getenv("VECTOR_STORE_ID") else []),
    get_weather,
]

agent = Agent(
    name="Tool Agent",
    instructions="Use tools when helpful. Cite sources when you searched the web.",
    tools=tools,
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "Compare today's weather in Warsaw vs. Berlin. Then search the web for top 2 coffee spots in each city.")
    print("\n=== FINAL OUTPUT ===\n", result.final_output)
```

## Run
```bash
python tool_agent.py
```

## References
- Agents SDK tools (function tools, web/file search).
