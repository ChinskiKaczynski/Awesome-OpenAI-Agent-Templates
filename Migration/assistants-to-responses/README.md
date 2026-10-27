# Assistants API → Responses API Migration

Complete migration guide with before/after examples.

> **Status:** The Assistants API was shut down on **August 26, 2026** and is no longer available. The `before/` example is retained for historical comparison only. See the [official migration guide](https://developers.openai.com/api/docs/assistants/migration).

## Quick Comparison

| Feature | Assistants API | Responses API |
|---------|---------------|---------------|
| **Threads** | Create/manage threads | `previous_response_id` or `conversation` |
| **Runs** | Create/poll runs | Single API call |
| **Tools** | Register tools | Built-in: `web_search`, `file_search`, etc. |
| **Files** | Upload → attach | `file_search` with vector stores |
| **Streaming** | SSE with run steps | SSE with structured events |
| **State** | Server-managed threads | `store: true` + chaining |

## Files

| File | Description |
|------|-------------|
| [before/assistant_example.py](./before/assistant_example.py) | Historical Assistants API code (no longer runnable) |
| [after/responses_example.py](./after/responses_example.py) | Migrated Responses API code |
| [MIGRATION_CHECKLIST.md](./MIGRATION_CHECKLIST.md) | Step-by-step checklist |

## Key Changes

### 1. Thread Management → Response Chaining

**Before (Assistants):**

```python
thread = client.beta.threads.create()
client.beta.threads.messages.create(thread_id=thread.id, role="user", content="Hello")
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
# Poll until complete...
```

**After (Responses):**

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Hello",
    store=True
)
# Chain with previous_response_id for follow-ups
```

### 2. File Retrieval → file_search Tool

**Before:**

```python
assistant = client.beta.assistants.create(
    tools=[{"type": "retrieval"}],
    file_ids=["file-abc123"]
)
```

**After:**

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Search the documents",
    tools=[{"type": "file_search", "vector_store_ids": ["vs_xxx"]}]
)
```

### 3. Code Interpreter → code_interpreter Tool

**Before:**

```python
assistant = client.beta.assistants.create(
    tools=[{"type": "code_interpreter"}]
)
```

**After:**

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Calculate something",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}]
)
```

## Run the Examples

```bash
# Historical `before/` example: reference only; the Assistants API is unavailable.
# Run only the Responses API example (requires an API key; API usage may be billed):
cd after
pip install openai python-dotenv
python responses_example.py
```

## Migration Risks

See [MIGRATION_CHECKLIST.md](./MIGRATION_CHECKLIST.md) for detailed risks and mitigations.
