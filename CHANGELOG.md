# Changelog

All notable changes to this repository will be documented in this file.

## [0.3.0] - 2026-01-08

### Added

- **Responses API templates** (`Responses-API/`):
  - `responses-minimal` - basic starter (Python + TypeScript)
  - `responses-streaming` - SSE streaming (Python + TypeScript)
  - `responses-store-conversation` - stateful conversations (Python + TypeScript)

- **Built-in Tools templates** (`Built-in-Tools/`):
  - `web-search-agent` - web search built-in tool
  - `file-search-agent` - file search with vector stores
  - `code-interpreter-agent` - sandboxed code execution

- **Agent Patterns** (`Agent-Patterns/`):
  - `routing-agent` - multi-agent routing with handoffs
  - `guardrails-io` - input/output validation
  - `agents-as-tools` - agent composition pattern
  - `parallel-agents` - concurrent execution

- **Realtime Voice GA** (`Realtime-Voice/`):
  - `websocket-minimal` - WebSocket starter (Python + JavaScript)
  - `webrtc-browser` - browser-based WebRTC voice agent

- **Migration Kit** (`Migration/`):
  - `assistants-to-responses` - before/after examples + checklist

- **Observability** (`Observability/`):
  - `tracing-otlp` - OpenTelemetry integration

- **Registry infrastructure**:
  - `registry.yml` - central template registry
  - `scripts/generate-readme.py` - README table generator

### Changed

- Updated `README.md` with:
  - Deprecation Timeline section
  - Expanded Template Registry table
  - New categories documentation
- Updated `Realtime-Voice/README.md` for GA API (`gpt-realtime`)

### Deprecated

- Assistants API templates (shutdown: Aug 26, 2026)
- Realtime API Beta (shutdown: Feb 27, 2026)
- `gpt-4o-realtime-preview` model (shutdown: Mar 24, 2026)

## [0.2.0] - 2025-10-20

### Added

- New repository structure with one-level categories: `agent-builder/`, `agents-sdk-python/`, `chatkit/`.
- New `README.md` with logo, badges, How to Use, Template Registry, Deprecated section, and ToC.
- CI workflow (`.github/workflows/link-check.yml`) to automatically validate external links.

### Changed

- Moved local templates from `templates/` into category folders.
- Updated `CONTRIBUTING.md` with English-only and status/verification rules.

### Removed

- **LICENSE** file (per maintainers' policy).

## [0.1.0] - 2025-10-19

- Initial commit with templates, guides, tutorials, and resources.
