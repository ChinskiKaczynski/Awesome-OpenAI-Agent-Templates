# Responses API - Streaming

Real-time streaming responses using Server-Sent Events (SSE).

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

1. Creates a streaming response request with `stream=True`
2. Iterates over SSE events in real-time
3. Prints text as it's generated (typewriter effect)

## Key Streaming Events

- `response.output_text.delta` - Text chunks as they're generated
- `response.completed` - Final response complete
- `error` - Any errors during generation

## Expected Output

```
🔄 Streaming response...
Hello! I'm an AI assistant...  (appears word by word)
✅ Complete! Total tokens: 42
```
