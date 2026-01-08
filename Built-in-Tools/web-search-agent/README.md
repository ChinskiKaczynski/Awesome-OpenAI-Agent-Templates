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

## What it does

1. Sends a query to the model with `web_search_preview` tool enabled
2. Model automatically searches the internet for current information
3. Returns answer synthesized from web results

## Example Queries

- "What is the current price of Bitcoin?"
- "Who won the latest Super Bowl?"
- "What are the top news headlines today?"

## Tool Options

| Tool Name | Description |
|-----------|-------------|
| `web_search_preview` | Standard web search (recommended) |
| `web_search` | Legacy web search |

## Expected Output

```
🔍 Query: Who is the current president of France?
🌐 Searching the web...
🤖 Answer: As of January 2026, Emmanuel Macron is the President of France...
```
