# Guardrails I/O Pattern

Demonstrate Agents SDK input/output tripwires with basic PII and keyword checks.

> This is an educational example, not a production safety filter. The checks block
> matching text; they do not redact sensitive data or reliably detect prompt
> injection or harmful content.

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
│   Input     │ ← Block matching PII patterns
│  Guardrail  │
└──────┬──────┘
       ↓
┌─────────────┐
│   Agent     │
└──────┬──────┘
       ↓
┌─────────────┐
│   Output    │ ← Block matching keywords
│  Guardrail  │
└──────┬──────┘
       ↓
   Response
```

## When to Use

- Learning how to block inputs matching simple PII patterns
- Learning how to block outputs matching simple keywords
- Understanding Agents SDK tripwire behavior

## Guardrail Types

| Type | Direction | Purpose |
|------|-----------|---------|
| Input | User → Agent | Block matching input |
| Output | Agent → User | Block matching output |

## Example Guardrails

1. **PII Detection**: Block text matching SSN, credit card, or email patterns.
2. **Output Keyword Check**: Block output containing a few example phrases.

These are illustrative heuristics, not comprehensive PII, injection, or moderation checks.
