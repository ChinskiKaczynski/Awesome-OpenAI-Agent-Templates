# Guardrails I/O Pattern

Validate inputs and sanitize outputs for safe agent interactions.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Pattern Overview

```
User Input
     ↓
┌─────────────┐
│   Input     │ ← Validate: no PII, no injection
│  Guardrail  │
└──────┬──────┘
       ↓
┌─────────────┐
│   Agent     │
└──────┬──────┘
       ↓
┌─────────────┐
│   Output    │ ← Sanitize: remove PII, check safety
│  Guardrail  │
└──────┬──────┘
       ↓
   Response
```

## When to Use

- Handling sensitive data (PII)
- Preventing prompt injection
- Enforcing output format
- Content moderation

## Guardrail Types

| Type | Direction | Purpose |
|------|-----------|---------|
| Input | User → Agent | Validate/sanitize input |
| Output | Agent → User | Check/filter response |

## Example Guardrails

1. **PII Detection**: Block SSN, credit cards
2. **Prompt Injection**: Detect manipulation attempts
3. **Format Validation**: Ensure JSON output
4. **Content Safety**: Filter harmful content
