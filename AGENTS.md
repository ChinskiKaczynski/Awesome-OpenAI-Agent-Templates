# AGENTS.md

Instructions for AI coding agents working with this repository.

> 📚 **Standard**: [agents.md](https://agents.md/)

## Repository Overview

This is **Awesome OpenAI Agent Templates** - a collection of educational starter templates for building AI agents using OpenAI APIs. Do not assume examples are production-ready without testing and review.

## Project Structure

```
├── Responses-API/          # Responses API templates
├── Built-in-Tools/         # Web search, file search, code interpreter, etc.
├── Agent-Patterns/         # Routing, guardrails, parallel agents
├── Realtime-Voice/         # WebSocket and WebRTC voice agents
├── Migration/              # API migration guides
├── Observability/          # Tracing and monitoring
├── Agents-SDK-Python/      # Python SDK example agents
├── ChatKit/                # Embeddable chat UI
├── registry.yml            # Central template registry
└── scripts/                # Utility scripts
```

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Primary language for agents |
| TypeScript | Alternative implementations |
| OpenAI SDK | `openai` Python/Node package |
| Agents SDK | `openai-agents` for agentic patterns |

## Key Files

- `registry.yml` - Central source of truth for templates
- `README.md` - Main documentation
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines

## Common Tasks

### Adding a New Template

1. Create folder: `CategoryName/template-name/`
2. Add `README.md` with usage instructions
3. Add language folders: `python/`, `typescript/`
4. Include `main.py` or `main.ts` with working example
5. Add `requirements.txt` or `package.json`
6. Update `registry.yml` with template metadata

### Template Structure

```
template-name/
├── README.md           # Required
├── python/
│   ├── main.py         # Main implementation
│   └── requirements.txt
└── typescript/
    ├── main.ts
    └── package.json
```

### Updating README

After modifying templates, run:

```bash
python scripts/generate-readme.py
```

## Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use ESM modules, async/await
- **Documentation**: Clear, concise READMEs

## Environment Variables

Required for all templates:

```
OPENAI_API_KEY=sk-...
```

Optional (template-specific):

```
VECTOR_STORE_ID=vs_...
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Testing Templates

```bash
# Python
cd template/python
pip install -r requirements.txt
python main.py

# TypeScript
cd template/typescript
npm install
npx tsx main.ts
```

## Verification

Before committing, ensure:

- [ ] Template runs without errors
- [ ] README has clear instructions
- [ ] `registry.yml` entry is added
- [ ] No hardcoded API keys
