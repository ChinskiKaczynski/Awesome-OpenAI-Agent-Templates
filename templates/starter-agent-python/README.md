# Starter Agent (Python, CLI)

Minimalny agent w Pythonie oparty o OpenAI SDK.

## Wymagania
- Python 3.10+
- `OPENAI_API_KEY` w `.env` lub w środowisku

## Setup
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../..//.env.example .env  # lub utwórz ręcznie
```

## Uruchomienie
```bash
python app.py
```

## Notatki
- Prosty REPL, zakończ `quit` aby wyjść.
