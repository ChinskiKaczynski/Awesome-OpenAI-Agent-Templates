# Tracing with OpenTelemetry (OTLP)

Export agent traces to any OpenTelemetry-compatible backend.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## What it does

1. Creates custom tracer using OpenTelemetry
2. Wraps agent execution with spans
3. Exports traces to configured backend

## Configuration

Set environment variables for your OTLP backend:

```bash
# For Jaeger (local)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=my-agent-app

# For cloud providers, add authentication
OTEL_EXPORTER_OTLP_HEADERS=api-key=xxx
```

## Running Jaeger Locally

```bash
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```

Then open <http://localhost:16686> to view traces.

## Trace Structure

```
agent_run (trace)
├── llm_generation (span)
│   └── model: gpt-4o-mini
├── tool_call (span)
│   └── tool: web_search
└── response (span)
    └── tokens: 150
```

## GenAI Semantic Conventions

We follow [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):

| Attribute | Description |
|-----------|-------------|
| `gen_ai.system` | AI system (openai) |
| `gen_ai.request.model` | Model used |
| `gen_ai.response.tokens` | Token count |
