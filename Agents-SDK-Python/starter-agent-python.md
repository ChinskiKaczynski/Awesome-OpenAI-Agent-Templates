# Starter Agent (Python)

## Overview
Minimal "hello agent" using the OpenAI Agents SDK for Python.

## Prerequisites
- Python 3.10+
- `OPENAI_API_KEY` set in your environment

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install openai-agents
```

## Example (`main.py`)

Save the following as `main.py`:

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

## Run
```bash
python main.py
```

## Links
- Agents SDK (Python): https://openai.github.io/openai-agents-python/
