# Awesome OpenAI Agent Templates (Reworked)

[![Stars](https://img.shields.io/github/stars/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates?style=flat)](https://github.com/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![CI](https://github.com/ChinskiKaczynski/Awesome-OpenAI-Agent-Templates/actions/workflows/ci.yml/badge.svg)](./.github/workflows/ci.yml)

> Produkcyjne szablony, tutoriale i wzorce do budowy agentów w oparciu o **OpenAI Agent Builder**, **Agents SDK (Python)** i **ChatKit**.

## Spis treści
- [Co jest w środku](#co-jest-w-środku)
- [Szybki start](#szybki-start)
- [Kategorie](#kategorie)
- [Szablony](#szablony)
- [Tutoriale i przewodniki](#tutoriale-i-przewodniki)
- [Wkład / Kontrybucje](#wkład--kontrybucje)
- [Licencja](#licencja)

## Co jest w środku
- **templates/** – uruchamialne szablony:
  - 🐍 `starter-agent-python/` – minimalny agent CLI (OpenAI Python SDK).
  - 🧰 `tool-calling-agent/` – funkcje narzędzi (calculator/web_search stub) + pętla.
  - 💬 `chatkit-ui-template/` – lekki frontend (Vite React) + prosty backend proxy do OpenAI.
- **agent-builder/** – README z instrukcją eksportu/importu workflowów z Agent Buildera.
- **guides/** – krótkie przewodniki (architektura, deploy, evals/guardrails).
- **.github/** – CI (lint/test/build), szablony PR/Issue.
- **.env.example** – przykład zmiennych środowiskowych.

> Źródła i najświeższe materiały: oficjalne dokumentacje OpenAI (Agents SDK, Agent Builder, ChatKit).

## Szybki start
1. Sklonuj repo i skopiuj `.env.example` → `.env`; ustaw `OPENAI_API_KEY`.
2. Wejdź do wybranego szablonu i uruchom zgodnie z instrukcją w jego `README.md`.
3. (Opcjonalnie) Odpal CI lokalnie: `ruff`, `black`, `pytest`.

## Kategorie
- **Agents SDK (Python)** – pętle, handoffy, narzędzia (function tools), sesje.
- **Agent Builder** – workflowy no‑code/low‑code; publikacja i integracja z ChatKit.
- **ChatKit** – osadzany interfejs czatu; hosting sesji i integracja z Agent Builderem.

## Szablony
| Szablon | Kiedy użyć | Jak uruchomić |
|---|---|---|
| `starter-agent-python` | Gdy chcesz minimalny, czytelny kod startowy | `cd templates/starter-agent-python && uv venv || python -m venv .venv && pip install -r requirements.txt && python app.py` |
| `tool-calling-agent` | Gdy chcesz użyć *function calling* i prostych narzędzi | `cd templates/tool-calling-agent && pip install -r requirements.txt && python app.py` |
| `chatkit-ui-template` | Gdy potrzebujesz UI + backend proxy | `cd templates/chatkit-ui-template && npm i && npm run dev` (backend: `npm run server`) |

## Tutoriale i przewodniki
Zajrzyj do katalogów **tutorials/** oraz **guides/** – krótkie materiały do startu i dobrych praktyk.

## Wkład / Kontrybucje
Zapraszamy do issue/PR — patrz [CONTRIBUTING.md](./CONTRIBUTING.md) i [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## Licencja
MIT. Zob. [LICENSE](./LICENSE).
