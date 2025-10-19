# Awesome-OpenAI-Agent-Templates

> Production-ready templates, tutorials, and patterns for building agents with **OpenAI Agent Builder**, **Agents SDK (Python)**, and **ChatKit**.

![Project Logo](./assets/logo-placeholder.png)

A curated, hands-on collection to go from idea to deployed agentic apps fast. Every template includes clear setup, runnable code (just add `OPENAI_API_KEY`), and links to official docs.

## Table of Contents
- [What’s Inside](#whats-inside)
- [Quick Start](#quick-start)
- [Categories](#categories)
- [Templates](#templates)
- [Tutorials](#tutorials)
- [Guides](#guides)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)

## What’s Inside
- **Templates:** starter Agents SDK (Python), tool-calling agent, and a ChatKit UI embed wired to Agent Builder.
- **Tutorials:** quickstart for Agent Builder, advanced workflows (handoffs, guardrails), step-by-step tool integration.
- **Guides:** deploy ChatKit on Vercel; architecture patterns for production agents.
- **Resources:** official docs, community showcases.

## Quick Start
1. **Clone** this repo.
2. Create `.env` and set:
   ```bash
   OPENAI_API_KEY=sk-...
   ```
3. Pick a template from [`templates/`](./templates) and follow its **Setup / Run** instructions.

> Note: Examples use OpenAI Agents SDK (Python) and ChatKit. Replace placeholder IDs (e.g., `VECTOR_STORE_ID`, `WORKFLOW_ID`) as instructed.

## Categories

- **Agents SDK (Python)**
  - Function tools, hosted tools (Web Search, File Search), sessions, handoffs, guardrails.
- **Agent Builder**
  - Visual workflows, publishing, integrating with ChatKit.
- **ChatKit**
  - Embeddable chat UI (hosted integration), session auth, theming, production tips.

## Templates
- [`templates/starter-agent-python.md`](./templates/starter-agent-python.md)
- [`templates/tool-calling-agent.md`](./templates/tool-calling-agent.md)
- [`templates/chatkit-ui-template.md`](./templates/chatkit-ui-template.md)

## Tutorials
- [`tutorials/quickstart-agent-builder.md`](./tutorials/quickstart-agent-builder.md)
- [`tutorials/advanced-agent-workflows.md`](./tutorials/advanced-agent-workflows.md)
- [`tutorials/integrating-tools-step-by-step.md`](./tutorials/integrating-tools-step-by-step.md)

## Guides
- [`guides/deploying-on-vercel.md`](./guides/deploying-on-vercel.md)
- [`guides/agent-architecture-patterns.md`](./guides/agent-architecture-patterns.md)

## Resources
- [`resources/official-docs-links.md`](./resources/official-docs-links.md)
- [`resources/community-showcases.md`](./resources/community-showcases.md)

## Contributing
We welcome issues and PRs. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the workflow.

## License
MIT — see [`LICENSE`](./LICENSE).

## Official Resources (selected)
- Agents SDK docs (Python): SDK primitives, tools, handoffs, guardrails.
- Built-in Tools (Web Search, File Search).
- ChatKit docs and sessions/auth guides.
- AgentKit / Agent Builder overview.
