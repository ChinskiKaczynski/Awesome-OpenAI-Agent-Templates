# Agent Patterns

Production-ready patterns for building complex AI agent systems using the **OpenAI Agents SDK**.

> 📚 **Official Docs**: [Agents SDK Python](https://openai.github.io/openai-agents-python/) | [Agents SDK JS](https://openai.github.io/openai-agents-js/)

## Available Patterns

| Pattern | Description | Complexity |
|---------|-------------|------------|
| [routing-agent](./routing-agent/) | Route requests to specialized agents | Intermediate |
| [guardrails-io](./guardrails-io/) | Input/output validation and safety | Intermediate |
| [agents-as-tools](./agents-as-tools/) | Use agents as tools for other agents | Advanced |
| [parallel-agents](./parallel-agents/) | Run multiple agents concurrently | Advanced |

## When to Use Each Pattern

### Routing Agent

Use when you have **multiple specialized agents** and need to route requests to the right one.

- Customer support (billing vs technical)
- Multi-domain assistants

### Guardrails I/O

Use when you need to **validate inputs and sanitize outputs**.

- PII detection
- Content moderation
- Format validation

### Agents as Tools

Use when you want **modular, composable agents**.

- Research + Analysis + Writing pipeline
- Multi-step workflows

### Parallel Agents

Use when tasks can be **executed concurrently**.

- Sentiment + Topic extraction in parallel
- Multiple data source queries

## Prerequisites

```bash
pip install openai-agents python-dotenv
```

## Quick Start

```bash
cd routing-agent
pip install -r requirements.txt
python main.py
```

## Agents SDK Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | LLM + instructions + tools |
| **Handoff** | Transfer control to another agent |
| **Guardrail** | Validate input/output |
| **Tool** | Function the agent can call |
| **Runner** | Executes the agent loop |
