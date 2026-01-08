# Routing Agent Pattern

Route incoming requests to specialized agents based on intent.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Pattern Overview

```
User Request
     ↓
┌─────────────┐
│  Triage     │
│  Agent      │
└──────┬──────┘
       │ handoff
   ┌───┴───┐
   ↓       ↓
┌─────┐  ┌─────┐
│Sales│  │Tech │
│Agent│  │Agent│
└─────┘  └─────┘
```

## When to Use

- Multi-domain customer support
- Specialized task handling
- Intent-based routing

## Key Concepts

1. **Triage Agent**: Analyzes request and hands off to specialist
2. **Handoff**: Transfer control + context to another agent
3. **Specialist Agents**: Domain-specific knowledge and tools

## Example Flow

```
User: "I want to upgrade my subscription"
→ Triage: Routes to Sales Agent
→ Sales Agent: Handles upgrade request

User: "My app is crashing"
→ Triage: Routes to Tech Support Agent
→ Tech Agent: Troubleshoots the issue
```
