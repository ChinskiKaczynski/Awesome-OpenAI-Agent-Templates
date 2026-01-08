# Observability Templates

Templates for **monitoring, tracing, and debugging** AI agents.

> 📚 **Official Docs**: [Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)

## Available Templates

| Template | Description | Complexity |
|----------|-------------|------------|
| [tracing-otlp](./tracing-otlp/) | OpenTelemetry integration | Intermediate |

## Why Observability?

Complex agent systems need visibility into:

- 🔍 **What tools were called** and with what arguments
- ⏱️ **How long each step took**
- 🔄 **Handoff patterns** between agents
- ❌ **Where failures occurred**

## Tracing Concepts

| Concept | Description |
|---------|-------------|
| **Span** | Single unit of work (tool call, LLM generation) |
| **Trace** | Complete request lifecycle (contains multiple spans) |
| **Attributes** | Metadata attached to spans |

## Integration Options

| Backend | Description |
|---------|-------------|
| OpenAI Dashboard | Built-in tracing (Agents SDK) |
| Jaeger | Open-source distributed tracing |
| Datadog | Enterprise APM |
| Honeycomb | Observability platform |

## Quick Start

```bash
cd tracing-otlp
pip install -r requirements.txt
python main.py
```
