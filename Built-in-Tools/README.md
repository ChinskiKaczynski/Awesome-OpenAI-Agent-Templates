# Built-in Tools Templates

Templates using **Responses API built-in tools** - powerful capabilities available natively without custom implementation.

> 📚 **Official Docs**: [Built-in Tools Guide](https://platform.openai.com/docs/guides/tools)

## Available Templates

| Template | Tool | Description | Difficulty |
|----------|------|-------------|------------|
| [web-search-agent](./web-search-agent/) | `web_search` | Real-time internet search | Beginner |
| [file-search-agent](./file-search-agent/) | `file_search` | RAG with vector stores | Intermediate |
| [code-interpreter-agent](./code-interpreter-agent/) | `code_interpreter` | Sandboxed code execution | Intermediate |

## Built-in Tools Overview

| Tool | Description | Use Case |
|------|-------------|----------|
| `web_search` / `web_search_preview` | Search the internet | Current events, facts, prices |
| `file_search` | Search uploaded documents | RAG, knowledge bases |
| `code_interpreter` | Execute Python in sandbox | Math, data analysis, charts |
| `computer_use` | Control virtual desktop | Browser automation, screenshots |

## Quick Start

```bash
# Python
cd web-search-agent/python
pip install -r requirements.txt
python main.py

# TypeScript
cd web-search-agent/typescript
npm install
npx tsx main.ts
```

## Key Concepts

### Combining Multiple Tools

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Analyze this data and visualize trends",
    tools=[
        {"type": "web_search_preview"},
        {"type": "file_search", "vector_store_ids": ["vs_xxx"]},
        {"type": "code_interpreter", "container": {"type": "auto"}}
    ]
)
```

### Tool Execution Flow

1. Model decides which tool(s) to use
2. Built-in tool executes automatically
3. Results returned to model
4. Model generates final response

## Related

- [Responses API Basics](../Responses-API/)
- [Agent Patterns](../Agent-Patterns/)
