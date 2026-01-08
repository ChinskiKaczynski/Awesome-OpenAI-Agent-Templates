# Computer Use Agent

Browser and desktop automation using the `computer_use_preview` built-in tool.

> ⚠️ **Preview Feature**: Computer use is currently in preview and may change.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## What it does

1. Launches a secure browser environment
2. Navigates to websites, clicks elements, fills forms
3. Takes screenshots and extracts information
4. Returns structured results

## Example Tasks

- "Go to Wikipedia and find the population of France"
- "Open Hacker News and get the top 5 headlines"
- "Search for 'OpenAI' on Google and summarize results"

## How It Works

```
User Task
    ↓
┌─────────────────┐
│  computer_use   │ ← Navigate, click, type, screenshot
│  preview        │
└────────┬────────┘
         ↓
   Extracted Data
```

## Safety Considerations

- ⚠️ Only use in sandboxed/isolated environments
- ⚠️ Never use with sensitive credentials
- ⚠️ Monitor all automated actions

## Environment Types

| Type | Description |
|------|-------------|
| `browser` | Web browser automation |
| `computer` | Full desktop environment |

## Limitations

- Preview feature, API may change
- Rate limited compared to other tools
- Complex UIs may require multiple attempts
