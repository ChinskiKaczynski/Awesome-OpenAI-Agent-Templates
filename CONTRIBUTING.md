# Contributing

Dziękujemy za chęć pomocy! Każdy nowy **template** powinien zawierać:
- uruchamialny kod + `README.md`,
- `.env.example`,
- screenshot/GIF (jeśli UI),
- prosty **smoke test** (`pytest` dla Pythona, `build` dla frontendu),
- zgodność z `ruff`/`black` (albo `eslint` dla JS).

## Jak zacząć
1. Fork > branch feature > commit (konwencja: `feat: ...`, `fix: ...`).
2. Uruchom lokalnie CI (`pre-commit`).
3. Otwórz PR i linkuj do Issue (jeśli jest).

## Definition of Done
- Template uruchamia się „z pudełka” po podaniu `OPENAI_API_KEY`.
- README jest zwięzły (setup, run, co robi).
- Testy „smoke” przechodzą.
