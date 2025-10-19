# Integrating Tools Step by Step

**Goal:** Add hosted Web/File Search and a custom function tool.

## 1) Web Search
```python
from agents import Agent, Runner, WebSearchTool

agent = Agent(
  name="Researcher",
  tools=[WebSearchTool()],
  instructions="Search and cite sources."
)
print(Runner.run_sync(agent, "Summarize the latest EU AI Act updates.").final_output)
```

## 2) File Search (Vector Stores)
- Create or reuse an OpenAI Vector Store, upload docs, and pass `vector_store_ids`.

```python
from agents import Agent, Runner, FileSearchTool
agent = Agent(
  name="RAG Bot",
  tools=[FileSearchTool(max_num_results=3, vector_store_ids=["VECTOR_STORE_ID"])],
)
print(Runner.run_sync(agent, "Answer using my uploaded policy PDFs only.").final_output)
```

## 3) Function Tool (Custom API)
```python
from typing_extensions import TypedDict
from agents import Agent, Runner, function_tool

class StockQuery(TypedDict):
    ticker: str

@function_tool
def get_price(q: StockQuery) -> str:
    """Return fake price for demo."""
    return f"{q['ticker']}: 123.45"

agent = Agent(name="Analyst", tools=[get_price])
print(Runner.run_sync(agent, "Get price for AAPL.").final_output)
```

## References
- Built-in tools guide; Agents SDK function tools.
