# Agent Architecture Patterns

This guide catalogs production patterns you can implement with **Agent Builder**, **Agents SDK**, and **ChatKit**.

## 1) Single Agent + Hosted Tools
- Use a single agent with **Web Search** and **File Search** for quick wins.
- Good for FAQs, policy Q&A, research digests.

## 2) Multi-Agent with Handoffs
- A triage agent hands off to domain specialists (billing, refunds, tech).
- Encodes clear responsibilities; improves interpretability.

## 3) Guardrails at the Edges
- Input guardrails to block abusive/unsupported intents.
- Output guardrails to prevent unsafe or off-policy responses.

## 4) RAG-first, Tools-second
- Prefer File Search on curated vector stores; fall back to Web Search if needed.

## 5) Observability & Iteration
- Use built-in tracing from the Agents SDK for debugging and evaluation.
- Short prompts, explicit tool descriptions, minimal hidden state.

## 6) Frontend Embedding via ChatKit
- Hostless UI path: OpenAI-hosted workflow + ChatKit + session token.
- Custom UI path: ChatKit server (advanced), or bespoke UI on top of Agents SDK.

## References
- Handoffs, guardrails, tools, and ChatKit docs.
