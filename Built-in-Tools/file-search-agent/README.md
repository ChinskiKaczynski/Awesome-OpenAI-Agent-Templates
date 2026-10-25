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

The Python and TypeScript examples print the query, vector store ID, and the model's answer. For example (answer text is illustrative):

```text
📚 Query: What are the main topics covered in the documents?
🔍 Searching vector store vs_abc123...
🤖 Answer: [Model-generated summary of the documents]
```

These examples return only `response.output_text`; they do **not** print a separate list of source filenames or relevance scores. To access ranked file-search results, add `include=["file_search_call.results"]` (Python) or `include: ["file_search_call.results"]` (TypeScript) to the Responses request and inspect `response.output`. See the [official file search guide](https://developers.openai.com/api/docs/guides/tools-file-search).

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
