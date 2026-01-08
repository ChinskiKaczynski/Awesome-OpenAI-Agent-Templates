# Personal Assistant Agent

An AI agent that helps manage tasks, schedules, and daily productivity.

## Features

- ✅ **Task Management**: Add, complete, and organize tasks
- 📅 **Scheduling**: Manage events and reminders
- 📝 **Notes**: Quick note-taking and retrieval
- 🎯 **Priorities**: Prioritize and categorize work
- 📊 **Daily Summary**: Generate daily overviews

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Example Commands

```
"Add a task: Review quarterly report by Friday"
"What's on my schedule for today?"
"Remind me to call the client at 3pm"
"Summarize my pending tasks"
"What are my high priority items?"
```

## Capabilities

| Capability | Description |
|------------|-------------|
| `add_task` | Create a new task with optional due date |
| `complete_task` | Mark a task as done |
| `list_tasks` | View tasks by status or priority |
| `add_event` | Schedule an event |
| `daily_summary` | Get overview of day |
| `take_note` | Save a quick note |

## Data Storage

Tasks and notes are stored in a local JSON file for persistence
between sessions. In production, connect to a calendar API or
database for real functionality.
