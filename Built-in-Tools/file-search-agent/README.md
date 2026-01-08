# File Search Agent

Document search using the `file_search` built-in tool with vector stores.

## Prerequisites

1. Create a vector store in the [OpenAI Dashboard](https://platform.openai.com/storage)
2. Upload your documents to the vector store
3. Copy the vector store ID (starts with `vs_`)

## Python

```bash
cd python
pip install -r requirements.txt
# Set your vector store ID in the code or as env var
python main.py
```

## TypeScript

```bash
cd typescript
npm install
npx tsx main.ts
```

## What it does

1. Connects to your vector store with uploaded documents
2. Searches documents semantically based on your query
3. Returns answer synthesized from relevant document chunks

## Example Use Cases

- Internal documentation search
- Customer support knowledge base
- Legal document analysis
- Research paper search

## Configuration

Set `VECTOR_STORE_ID` environment variable or edit the code:

```bash
export VECTOR_STORE_ID=vs_abc123...
```

## Expected Output

```
📚 Searching documents: What is our refund policy?
🔍 Searching vector store vs_abc123...
🤖 Answer: According to our documentation, the refund policy states...

📄 Sources:
   - refund-policy.pdf (relevance: 0.92)
   - faq.md (relevance: 0.85)
```

## Creating a Vector Store

```python
# via API:
vector_store = client.vector_stores.create(name="My Knowledge Base")
print(f"Created: {vector_store.id}")

# Upload files:
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id="file-abc123"
)
```
