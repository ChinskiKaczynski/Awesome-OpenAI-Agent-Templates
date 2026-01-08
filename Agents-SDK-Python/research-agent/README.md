# Research Agent

An AI agent that searches for information and synthesizes it into comprehensive reports.

## Features

- 🔍 **Web Search**: Searches the internet for current information
- 📊 **Source Evaluation**: Ranks sources by relevance and reliability
- 📝 **Synthesis**: Combines findings into structured reports
- 📚 **Citation**: Includes sources for all claims

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Example Queries

```
"Research the latest developments in fusion energy"
"Compare React vs Vue for enterprise applications"
"What are the health benefits of intermittent fasting?"
```

## How It Works

```
User Query
    ↓
┌─────────────┐
│ Query       │ ← Break down into sub-questions
│ Planner     │
└──────┬──────┘
       ↓
┌─────────────┐
│ Research    │ ← Search web, evaluate sources
│ Tool        │
└──────┬──────┘
       ↓
┌─────────────┐
│ Synthesizer │ ← Combine and format
└──────┬──────┘
       ↓
  Final Report
```

## Output Format

```markdown
# Research Report: [Topic]

## Executive Summary
...

## Key Findings
1. ...
2. ...

## Detailed Analysis
...

## Sources
- [Source 1](url)
- [Source 2](url)
```
