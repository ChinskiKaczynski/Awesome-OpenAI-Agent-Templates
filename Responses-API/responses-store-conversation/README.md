# Responses API - Stateful Conversations

Multi-turn conversations using stored responses and `previous_response_id`.

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

## What it does

1. Creates a response with `store=True` (stored on OpenAI servers)
2. Passes `previous_response_id` to continue the conversation
3. Reuses earlier context without manually resending the messages

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `store=True` | Stores the response for retrieval (response objects are retained for 30 days by default) |
| `previous_response_id` | Chains a response to the previous one; prior input tokens are still billed |
| `conversation` | ID of a durable Conversation object created with the Conversations API |

## Expected Output

```
👤 User: Tell me a joke
🤖 Assistant: Why don't scientists trust atoms? Because they make up everything!

👤 User: Explain why it's funny
🤖 Assistant: The joke is a pun playing on the double meaning of "make up"...
```

## Alternative: Durable Conversations

For conversation state that can be reused across sessions, create a Conversation object first, then pass its ID on each turn:

```python
from openai import OpenAI

client = OpenAI()
conversation = client.conversations.create()

first = client.responses.create(
    model="gpt-4o-mini",
    input="Hello! My favorite color is blue.",
    conversation=conversation.id,
)
second = client.responses.create(
    model="gpt-4o-mini",
    input="What is my favorite color?",
    conversation=conversation.id,
)
print(second.output_text)
print(f"Save this conversation ID to continue later: {conversation.id}")
```

Save the returned `conversation.id` in your application if you need to resume later. Do not use `previous_response_id` together with `conversation` in the same request.

## Notes

- Both approaches avoid manually resending the entire message history.
- Stored response objects have a default 30-day retention period; Conversation objects and their items are not subject to that TTL.
- Conversation state does **not** automatically manage the model's context window. Long conversations may require explicit context management or compaction.
- Earlier input tokens in a `previous_response_id` chain are still billed.

Official reference: [OpenAI Conversation State](https://platform.openai.com/docs/guides/conversation-state)
