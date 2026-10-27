# Responses API - Stateful Conversations

Multi-turn conversations with automatic context management using `store=true` and `previous_response_id`.

## Python

```bash
cd python
pip install -r requirements.txt
python main.py
```

## TypeScript

```bash
cd typescript
npm install
npx tsx main.ts
```

Requires Node.js 20.12+ for optional `.env` loading. Alternatively, set `OPENAI_API_KEY` in your shell.

## What it does

1. Creates first response with `store=True` (persists on OpenAI servers)
2. Uses `previous_response_id` to chain follow-up messages
3. Model maintains full conversation context automatically

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `store=True` | Persist response for later retrieval |
| `previous_response_id` | Chain to previous response for context |
| `conversation` | Alternative: named conversation identifier |

## Expected Output

```
👤 User: Tell me a joke
🤖 Assistant: Why don't scientists trust atoms? Because they make up everything!

👤 User: Explain why it's funny
🤖 Assistant: The joke is a pun playing on the double meaning of "make up"...
```

## Alternative: Named Conversations

```python
# Instead of previous_response_id, use named conversations:
response = client.responses.create(
    model="gpt-4o-mini",
    input="Hello!",
    conversation="conv_my-chat-session"
)
```

## Benefits

- ✅ No need to manage conversation history manually
- ✅ Automatic token management
- ✅ Persistent across sessions (with store=True)
