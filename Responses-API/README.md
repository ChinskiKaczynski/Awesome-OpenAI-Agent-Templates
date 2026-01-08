# Responses API Templates

Production-ready templates for OpenAI's **Responses API** - the recommended foundation for new projects (2025+).

> 📚 **Official Docs**: [Responses API Guide](https://platform.openai.com/docs/guides/responses)

## Templates

| Template | Description | Difficulty |
|----------|-------------|------------|
| [responses-minimal](./responses-minimal/) | Basic input/output starter | Beginner |
| [responses-streaming](./responses-streaming/) | Real-time SSE streaming | Beginner |
| [responses-store-conversation](./responses-store-conversation/) | Stateful multi-turn conversations | Intermediate |

## Why Responses API?

The Responses API is OpenAI's newest and most advanced API, combining the best of:

- **Chat Completions API** - Simple request/response
- **Assistants API** - Stateful conversations and tools

### Key Features

- **Built-in tools**: `web_search`, `file_search`, `code_interpreter`, `computer_use`
- **Stateful conversations**: Use `store: true` + `previous_response_id`
- **Agentic by default**: Multi-tool calls in single request
- **Streaming**: Rich SSE events for real-time UX

## Quick Start

```bash
# Python
cd responses-minimal/python
pip install openai python-dotenv
python main.py

# TypeScript
cd responses-minimal/typescript
npm install
npx tsx main.ts
```

## Environment Setup

Create `.env` file:

```
OPENAI_API_KEY=sk-...
```

## Related

- [Responses vs Chat Completions](https://platform.openai.com/docs/guides/responses-vs-chat-completions)
- [Assistants → Responses Migration](../Migration/assistants-to-responses/)
