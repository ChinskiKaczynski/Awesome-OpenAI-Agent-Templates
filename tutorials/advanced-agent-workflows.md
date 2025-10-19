# Advanced Agent Workflows (Agents SDK)

**Goal:** Compose multi-agent systems with **handoffs**, enforce **guardrails**, and mix hosted + function tools.

## Handoffs
```python
from agents import Agent, handoff, Runner

billing = Agent(name="Billing agent")
refunds = Agent(name="Refunds agent")

triage = Agent(
    name="Triage",
    instructions="Route to billing or refunds based on the user's intent.",
    handoffs=[billing, handoff(refunds)]
)

if __name__ == "__main__":
    r = Runner.run_sync(triage, "I need to dispute a charge.")
    print(r.final_output)
```

## Guardrails
```python
from pydantic import BaseModel
from agents import (
  Agent, Runner, RunContextWrapper, input_guardrail,
  GuardrailFunctionOutput, InputGuardrailTripwireTriggered
)

class AbuseCheck(BaseModel):
    abusive: bool
    reason: str

moderation = Agent(
    name="Moderation",
    instructions="Check if input is abusive. Respond with abusive=true/false.",
    output_type=AbuseCheck,
)

@input_guardrail
async def abuse_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str):
    res = await Runner.run(moderation, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=res.final_output, tripwire_triggered=res.final_output.abusive
    )

support = Agent(name="Support", input_guardrails=[abuse_guardrail])

try:
    out = Runner.run_sync(support, "You're terrible. Help me anyway.")
    print(out.final_output)
except InputGuardrailTripwireTriggered:
    print("Blocked by guardrail")
```

## Hosted + Function Tools
- Add `WebSearchTool()` and `FileSearchTool(...)`, then **@function_tool** to wrap your own API calls.
- Start with hosted tools, then evolve to function tools for business systems.

## References
- Handoffs and guardrails docs.
