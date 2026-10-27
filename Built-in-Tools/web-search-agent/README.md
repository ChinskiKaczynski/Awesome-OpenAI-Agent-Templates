# Web Search Agent

Real-time internet search using the `web_search` built-in tool.

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

The examples use `gpt-4.1-mini` and require `OPENAI_API_KEY`. Live API calls and web searches may incur usage charges.

See the [official web search guide](https://developers.openai.com/api/docs/guides/tools-web-search) for supported options.

## What it does

1. Sends a query to the model with `web_search` tool enabled
2. Model automatically searches the internet for current information
3. Validates the completed search and citation metadata; prints the answer and deduplicated HTTP(S) source URLs (Python and TypeScript). This confirms URLs were cited, not that every claim is true.

## Example Queries

- "What is the current price of Bitcoin?"
- "Who won the latest Super Bowl?"
- "What are the top news headlines today?"

## Tool Options

| Tool Name | Description |
|-----------|-------------|
| `web_search` | Stable web search (recommended) |
| `web_search_preview` | Legacy web search (for existing integrations) |

## Expected Output

```
🔍 Query: Who is the current president of France?
🌐 Searching the web...
🤖 Answer: <answer with source citations>...
Sources:
- https://example.org/source
```
