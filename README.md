<p align="center">
  <img src="./logo.png" alt="Awesome OpenAI Agent Templates" width="640" />
</p>

<h1 align="center">Awesome OpenAI Agent Templates</h1>

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://github.com/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates?style=social"></a>
  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates">
  <a href="https://github.com/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates/pulls"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
</p>

> Starter templates, tutorials, and patterns for building agents with the **Responses API**, **Agents SDK**, **Realtime API**, and more. Examples are educational and require testing and review before production use.

---

## Table of Contents

- [Overview](#overview)
- [⚠️ Deprecation Timeline](#️-deprecation-timeline)
- [How to Use](#how-to-use)
- [Categories](#categories)
- [Template Registry](#template-registry)
- [Deprecated Templates](#deprecated-templates)
- [Contribute](#contribute)
- [Changelog](#changelog)

## Overview

This repository curates runnable templates and high-quality references so you can go from idea to deployed agentic apps fast. Each template includes:

- **Clear setup** and **run** instructions,
- Pointers to **official docs** for deeper learning,
- Minimal placeholders (`OPENAI_API_KEY`, `VECTOR_STORE_ID`, etc.).

## ⚠️ Deprecation Timeline

> **Important dates to plan your migrations:**

| API/Model | Deprecation Date | Replacement | Migration Guide |
|-----------|------------------|-------------|-----------------|
| **Assistants API** | **Aug 26, 2026** | Responses API | [Migration Kit](./Migration/assistants-to-responses/) |
| Realtime API Beta | Feb 27, 2026 | Realtime API GA | [Realtime Voice](./Realtime-Voice/) |
| gpt-4o-realtime-preview | Mar 24, 2026 | gpt-realtime | [Realtime Voice](./Realtime-Voice/) |

## How to Use

1. **Pick a category** under the repo root:
   - `Responses-API/` – Responses API starters (stateful, streaming, tools),
   - `Built-in-Tools/` – web search, file search, code interpreter,
   - `Agent-Patterns/` – routing, guardrails, parallel agents,
   - `Realtime-Voice/` – WebSocket and WebRTC voice agents,
   - `Migration/` – migration guides (Assistants → Responses),
   - `Observability/` – tracing and monitoring,
   - `Agents-SDK-Python/` – Python SDK templates,
   - `ChatKit/` – links to official ChatKit UI starters and documentation.

2. **Install dependencies** as described by each template (Python venv / Node, etc.).

3. **Create a `.env`** (when needed) and set:

   ```bash
   OPENAI_API_KEY=sk-...
   ```

4. **Run** the template (instructions inside each template's README).

> Official docs (recommended):  
>
> - Responses API: <https://platform.openai.com/docs/guides/responses>  
> - Agents SDK (Python): <https://openai.github.io/openai-agents-python/>  
> - Agents SDK (TypeScript): <https://openai.github.io/openai-agents-js/>  
> - Realtime API: <https://platform.openai.com/docs/guides/realtime>  
> - ChatKit: <https://platform.openai.com/docs/guides/chatkit>

## Categories

| Category | Description | Templates |
|----------|-------------|-----------|
| **Responses API** | Next-gen API for agents | 3 starters |
| **Built-in Tools** | Web search, file search, code interpreter, computer use, MCP | 5 templates |
| **Agent Patterns** | Routing, guardrails, composition | 4 patterns |
| **Realtime Voice** | Low-latency voice agents | 2 templates |
| **Migration** | API migration guides | 1 guide |
| **Observability** | Tracing and monitoring | 1 template |
| **Agents SDK** | Python/TypeScript SDK | 8 templates |
| **ChatKit** | Official UI examples and docs | 1 reference |

## Template Registry

> ✅ = Legacy `verified` registry label (not evidence of live testing or production readiness), 🔄 = Reference or unverified, 📁 = Local template, 🔗 = External link

<!-- REGISTRY_TABLE_START -->

| Template | Category | Languages | Difficulty | Status | Description |
|----------|----------|-----------|------------|--------|-------------|
| 📁 [Responses API Minimal](Responses-API/responses-minimal/) | Responses API | python, typescript | Beginner | ✅ | Basic Responses API starter with simple input/output |
| 📁 [Responses API Streaming](Responses-API/responses-streaming/) | Responses API | python, typescript | Beginner | ✅ | Streaming responses with SSE events |
| 📁 [Stateful Conversations](Responses-API/responses-store-conversation/) | Responses API | python, typescript | Intermediate | ✅ | Multi-turn conversations with store=true and previous_response_id |
| 📁 [Web Search Agent](Built-in-Tools/web-search-agent/) | Built-in Tools | python, typescript | Beginner | ✅ | Real-time web search using built-in web_search tool |
| 📁 [File Search Agent](Built-in-Tools/file-search-agent/) | Built-in Tools | python, typescript | Intermediate | ✅ | Document search with vector stores |
| 📁 [Code Interpreter Agent](Built-in-Tools/code-interpreter-agent/) | Built-in Tools | python, typescript | Intermediate | ✅ | Code execution in sandbox environment |
| 📁 [Realtime WebSocket Minimal](Realtime-Voice/websocket-minimal/) | Realtime Voice | python, javascript | Intermediate | ✅ | Minimal WebSocket voice agent with gpt-realtime |
| 📁 [Realtime WebRTC Browser](Realtime-Voice/webrtc-browser/) | Realtime Voice | javascript | Advanced | 🔄 | Browser WebRTC SDP-offer scaffold; session handshake not implemented |
| 📁 [Routing Agent](Agent-Patterns/routing-agent/) | Agent Patterns | python | Intermediate | ✅ | Multi-agent routing and delegation pattern |
| 📁 [Input/Output Guardrails](Agent-Patterns/guardrails-io/) | Agent Patterns | python | Intermediate | ✅ | Input validation and output safety checks |
| 📁 [Agents as Tools](Agent-Patterns/agents-as-tools/) | Agent Patterns | python | Advanced | ✅ | Agent composition - using agents as tools |
| 📁 [Parallel Agents](Agent-Patterns/parallel-agents/) | Agent Patterns | python | Advanced | ✅ | Concurrent agent execution with result aggregation |
| 📁 [Assistants → Responses Migration](Migration/assistants-to-responses/) | Migration | python | Intermediate | ✅ | Before/after examples migrating from Assistants API |
| 📁 [Tracing with OTLP](Observability/tracing-otlp/) | Observability | python | Intermediate | ✅ | OpenTelemetry integration for agent tracing |
| 📁 [Starter Agent (Python)](Agents-SDK-Python/) | Agents SDK (Python) | python | Beginner | ✅ | Minimal "hello agent" with tools and tracing |
| 📁 [Tool-calling Agent](Agents-SDK-Python/) | Agents SDK (Python) | python | Beginner | 🔄 | Reference to Agents SDK function tools; no runnable script |
| 📁 [Research Agent](Agents-SDK-Python/research-agent/) | Agents SDK (Python) | python | Intermediate | 🔄 | Responses web search and API citation URLs; live search not verified |
| 📁 [Customer Support Agent](Agents-SDK-Python/customer-support-agent/) | Agents SDK (Python) | python | Intermediate | 🔄 | Offline scripted-SDK handoff tested; live routing not verified |
| 📁 [Data Analyst Agent](Agents-SDK-Python/data-analyst-agent/) | Agents SDK (Python) | python | Advanced | ✅ | Analyzes data and generates insights |
| 📁 [Content Writer Agent](Agents-SDK-Python/content-writer-agent/) | Agents SDK (Python) | python | Intermediate | ✅ | Writes blog posts, emails, and marketing copy |
| 📁 [Personal Assistant Agent](Agents-SDK-Python/personal-assistant-agent/) | Agents SDK (Python) | python | Advanced | ✅ | Task management and scheduling agent |
| 📁 [Code Review Agent](Agents-SDK-Python/code-review-agent/) | Agents SDK (Python) | python | Advanced | ✅ | Reviews code and suggests improvements |
| 📁 [ChatKit UI References](ChatKit/) | ChatKit |  | Beginner | 🔄 | Links to official ChatKit docs and starters; no local runnable embed |

### External Resources

| Resource | Category | Description |
|----------|----------|-------------|
| 🔗 [Realtime Voice Agents Demo](https://github.com/openai/openai-realtime-agents) | Realtime Voice | Advanced patterns for low-latency voice agents |
| 🔗 [Agents SDK Python Examples](https://openai.github.io/openai-agents-python/examples/) | Agents SDK (Python) | Category-organized examples from OpenAI |
| 🔗 [Agents SDK TypeScript](https://openai.github.io/openai-agents-js/) | Agents SDK (TypeScript) | TypeScript SDK docs & examples |
| 🔗 [Temporal Durable Agents Demos](https://github.com/temporal-community/openai-agents-demos) | Agent Patterns | Durable execution patterns with Agents SDK |

<!-- REGISTRY_TABLE_END -->

**Registry table updated:** 2026-10-26 (not a runtime verification date; consult `registry.yml` for the current template inventory).

## Deprecated Templates

- **Swarm-based templates** → **Deprecated**. Use the **OpenAI Agents SDK** (the production-ready evolution of Swarm).  

- **Assistants API-based templates** → **Deprecated** (shutdown **Aug 26, 2026**).  
  *Prefer:* **Responses API** + **Agents SDK**, or use the [Migration Kit](./Migration/assistants-to-responses/).

> See `Deprecated/` for migration notes and links.

## Contribute

We welcome high-signal templates, guides, and updates. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a PR.  
All content must be **English-only**. Add a minimal README for every template and include run instructions.

## Registry

Templates are defined in [`registry.yml`](./registry.yml). Run `python scripts/generate-readme.py` to update the table above.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
