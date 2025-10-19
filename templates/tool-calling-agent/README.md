# Tool‑Calling Agent (Python)

Przykład użycia **function calling** z dwiema funkcjami:
- `calculator.add(a, b)`
- `web_search.search(query)` (stub – zwraca przykładowe wyniki lokalnie)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../..//.env.example .env
python app.py
```
