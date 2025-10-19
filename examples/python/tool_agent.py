import os
from typing_extensions import TypedDict
from agents import Agent, Runner, WebSearchTool, FileSearchTool, function_tool

class WeatherQuery(TypedDict):
    city: str
    unit: str  # "celsius" or "fahrenheit"

@function_tool
def get_weather(q: WeatherQuery) -> str:
    temp_c = 20
    if q.get("unit") == "fahrenheit":
        temp_f = temp_c * 9/5 + 32
        return f"{q['city']}: {temp_f:.1f} °F, clear"
    return f"{q['city']}: {temp_c} °C, clear"

tools = [
    WebSearchTool(),
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
