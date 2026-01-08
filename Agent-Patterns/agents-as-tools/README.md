# Agents as Tools Pattern

Use agents as tools for other agents, enabling modular composition.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Pattern Overview

```
┌─────────────────┐
│  Orchestrator   │
│     Agent       │
└────────┬────────┘
         │ uses as tools
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌───────┐
│Research│ │Writer │
│ Agent  │ │ Agent │
└───────┘ └───────┘
```

## When to Use

- Multi-step workflows (research → analyze → write)
- Modular, reusable agent components
- Complex tasks requiring different expertise

## Key Concepts

1. **Orchestrator**: Main agent that coordinates work
2. **Tool Agents**: Specialized agents exposed as tools
3. **Composition**: Combine capabilities flexibly

## Example Flow

```
User: "Write a blog post about quantum computing"

Orchestrator:
  1. Calls Research Agent tool → gets facts
  2. Calls Writer Agent tool → generates draft
  3. Returns polished blog post
```

## Benefits

- 🧩 **Modular**: Each agent has single responsibility
- 🔄 **Reusable**: Tool agents can be used elsewhere
- 🎯 **Focused**: Each agent optimized for its task
