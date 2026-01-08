"""
Tracing with OpenTelemetry (OTLP)
Export agent traces to any OpenTelemetry-compatible backend.

Prerequisites:
    pip install openai opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
    
    Optional: Run Jaeger locally for visualization
    docker run -d -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

load_dotenv()

# ============================================
# OpenTelemetry Setup
# ============================================

# Configure resource (service info)
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "openai-agent-demo"),
    "service.version": "1.0.0",
})

# Create tracer provider
provider = TracerProvider(resource=resource)

# Configure OTLP exporter (sends to Jaeger, Datadog, etc.)
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)

# Add batch processor for efficient export
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Set global tracer provider
trace.set_tracer_provider(provider)

# Get tracer
tracer = trace.get_tracer(__name__)

# OpenAI client
client = OpenAI()


# ============================================
# Traced Agent Functions
# ============================================

def traced_response_create(model: str, prompt: str) -> str:
    """
    Create a response with OpenTelemetry tracing.
    
    This wraps the OpenAI call with a span that captures:
    - Model used
    - Prompt (truncated)
    - Token usage
    - Duration
    """
    with tracer.start_as_current_span("llm_generation") as span:
        # Add GenAI semantic attributes
        span.set_attribute("gen_ai.system", "openai")
        span.set_attribute("gen_ai.request.model", model)
        span.set_attribute("gen_ai.prompt", prompt[:100])  # Truncate for safety
        
        try:
            response = client.responses.create(
                model=model,
                input=prompt,
            )
            
            # Record response attributes
            span.set_attribute("gen_ai.response.id", response.id)
            span.set_attribute("gen_ai.usage.total_tokens", response.usage.total_tokens)
            span.set_attribute("gen_ai.usage.prompt_tokens", response.usage.input_tokens)
            span.set_attribute("gen_ai.usage.completion_tokens", response.usage.output_tokens)
            
            return response.output_text
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR, str(e))
            raise


def traced_tool_call(tool_name: str, args: dict = None):
    """
    Trace a tool call.
    """
    with tracer.start_as_current_span(f"tool_call.{tool_name}") as span:
        span.set_attribute("tool.name", tool_name)
        if args:
            span.set_attribute("tool.arguments", str(args))
        
        # Simulate tool execution
        import time
        time.sleep(0.1)
        
        span.set_attribute("tool.status", "success")
        return f"Tool {tool_name} executed successfully"


# ============================================
# Demo Agent Run
# ============================================

def run_traced_agent(user_query: str):
    """
    Run an agent with full tracing.
    """
    with tracer.start_as_current_span("agent_run") as span:
        span.set_attribute("agent.query", user_query)
        
        print(f"🔍 Processing: {user_query}")
        
        # Step 1: Analyze intent (could be LLM call)
        with tracer.start_as_current_span("analyze_intent"):
            print("  📊 Analyzing intent...")
            # Simulated
        
        # Step 2: Tool calls
        tool_result = traced_tool_call("web_search", {"query": user_query})
        print(f"  🔧 {tool_result}")
        
        # Step 3: Generate response
        response = traced_response_create(
            model="gpt-4o-mini",
            prompt=f"Based on search results, answer: {user_query}"
        )
        
        span.set_attribute("agent.response_length", len(response))
        
        print(f"  ✅ Response generated ({len(response)} chars)")
        
        return response


def main():
    """Demo tracing with sample queries."""
    
    print("=" * 50)
    print("OpenTelemetry Tracing Demo")
    print(f"Exporting to: {otlp_endpoint}")
    print("=" * 50 + "\n")
    
    queries = [
        "What is the capital of France?",
        "Explain quantum computing briefly",
    ]
    
    for query in queries:
        result = run_traced_agent(query)
        print(f"\n📝 Result: {result[:100]}...")
        print("-" * 50 + "\n")
    
    # Flush traces
    provider.force_flush()
    
    print("✅ Traces exported!")
    print("   View at: http://localhost:16686 (if using Jaeger)")


if __name__ == "__main__":
    main()
