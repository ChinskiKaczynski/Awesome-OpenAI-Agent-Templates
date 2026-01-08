# Agents SDK Python - Example Agents

Production-ready example agents built with the **OpenAI Agents SDK**.

> 📚 **Official Docs**: [Agents SDK Python](https://openai.github.io/openai-agents-python/)

## Example Agents

| Agent | Description | Difficulty |
|-------|-------------|------------|
| [research-agent](./research-agent/) | Search, synthesize, and summarize information | Intermediate |
| [customer-support-agent](./customer-support-agent/) | Handle support tickets with routing | Intermediate |
| [data-analyst-agent](./data-analyst-agent/) | Analyze data and generate insights | Advanced |
| [content-writer-agent](./content-writer-agent/) | Write blog posts, emails, marketing copy | Intermediate |
| [personal-assistant-agent](./personal-assistant-agent/) | Task management and scheduling | Advanced |
| [code-review-agent](./code-review-agent/) | Review code and suggest improvements | Advanced |

## Getting Started

```bash
# Install Agents SDK
pip install openai-agents python-dotenv

# Set your API key
export OPENAI_API_KEY=sk-...

# Run any agent
cd research-agent
python main.py
```

## Agents SDK Core Concepts

```python
from agents import Agent, Runner, function_tool

# Define a tool
@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 22°C"

# Create an agent
agent = Agent(
    name="Weather Assistant",
    instructions="Help users with weather queries.",
    tools=[get_weather],
)

# Run the agent
result = await Runner.run(agent, "What's the weather in Paris?")
print(result.final_output)
```

## Legacy Templates

- [starter-agent-python.md](./starter-agent-python.md) - Original minimal starter
- [tool-calling-agent.md](./tool-calling-agent.md) - Tool calling demo
