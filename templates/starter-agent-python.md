# Starter Agent (Python, Agents SDK)

**Goal:** Minimal agent using **OpenAI Agents SDK** with a single model and no tools — then extendable.

## Setup
```bash
pip install openai-agents openai python-dotenv
export OPENAI_API_KEY=sk-...
```

## Run
Create `starter.py` with the code below and run:
```bash
python starter.py
```

## Example code
```python
# starter.py
import os
from agents import Agent, Runner

# Ensure OPENAI_API_KEY is set in the environment
# e.g., export OPENAI_API_KEY=sk-...

agent = Agent(
    name="Assistant",
    instructions="You are a concise, helpful assistant."
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "Give me 3 bullet points on unit testing best practices.")
    print(result.final_output)
```

## Notes
- Uses Agents SDK primitives (Agent, Runner). Extend by adding tools or handoffs later.
- Official docs: Agents SDK Intro, Hello world, and Quickstart.
