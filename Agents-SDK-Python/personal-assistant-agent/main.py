"""
Personal Assistant Agent
An AI agent that helps manage tasks, schedules, and daily productivity.

Uses function tools for task and schedule management.
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from agents import Agent, Runner, function_tool


# Data file for persistence
DATA_FILE = Path("assistant_data.json")


@dataclass
class Task:
    """A task item."""
    id: str
    title: str
    due_date: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    status: str = "pending"  # pending, completed
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class Note:
    """A quick note."""
    id: str
    content: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


# In-memory storage
tasks: list[Task] = []
notes: list[Note] = []


def load_data():
    """Load data from file."""
    global tasks, notes
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text())
        tasks = [Task(**t) for t in data.get("tasks", [])]
        notes = [Note(**n) for n in data.get("notes", [])]


def save_data():
    """Save data to file."""
    data = {
        "tasks": [asdict(t) for t in tasks],
        "notes": [asdict(n) for n in notes]
    }
    DATA_FILE.write_text(json.dumps(data, indent=2))


# ============================================
# Tool Functions
# ============================================

@function_tool
def add_task(title: str, due_date: str = None, priority: str = "medium") -> str:
    """
    Add a new task to the task list.
    
    Args:
        title: The task description
        due_date: Optional due date (format: YYYY-MM-DD)
        priority: Task priority (low, medium, high)
    
    Returns:
        Confirmation message
    """
    task_id = f"task_{len(tasks) + 1}"
    task = Task(id=task_id, title=title, due_date=due_date, priority=priority)
    tasks.append(task)
    save_data()
    
    due_str = f" (due: {due_date})" if due_date else ""
    return f"✅ Added task: '{title}'{due_str} [{priority} priority]"


@function_tool
def complete_task(task_id: str) -> str:
    """
    Mark a task as completed.
    
    Args:
        task_id: The ID of the task to complete
    
    Returns:
        Confirmation message
    """
    for task in tasks:
        if task.id == task_id:
            task.status = "completed"
            save_data()
            return f"✅ Completed: '{task.title}'"
    
    return f"❌ Task not found: {task_id}"


@function_tool
def list_tasks(status: str = "all", priority: str = "all") -> str:
    """
    List tasks with optional filtering.
    
    Args:
        status: Filter by status (all, pending, completed)
        priority: Filter by priority (all, low, medium, high)
    
    Returns:
        Formatted task list
    """
    filtered = tasks
    
    if status != "all":
        filtered = [t for t in filtered if t.status == status]
    
    if priority != "all":
        filtered = [t for t in filtered if t.priority == priority]
    
    if not filtered:
        return "📋 No tasks found matching criteria."
    
    lines = ["📋 Tasks:"]
    for task in filtered:
        status_icon = "✅" if task.status == "completed" else "⬜"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "")
        due_str = f" (due: {task.due_date})" if task.due_date else ""
        lines.append(f"  {status_icon} {priority_icon} [{task.id}] {task.title}{due_str}")
    
    return "\n".join(lines)


@function_tool
def take_note(content: str) -> str:
    """
    Save a quick note.
    
    Args:
        content: The note content
    
    Returns:
        Confirmation message
    """
    note_id = f"note_{len(notes) + 1}"
    note = Note(id=note_id, content=content)
    notes.append(note)
    save_data()
    
    return f"📝 Note saved: '{content[:50]}...'" if len(content) > 50 else f"📝 Note saved: '{content}'"


@function_tool
def list_notes() -> str:
    """
    List all notes.
    
    Returns:
        Formatted note list
    """
    if not notes:
        return "📝 No notes found."
    
    lines = ["📝 Notes:"]
    for note in notes[-10:]:  # Last 10 notes
        preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
        lines.append(f"  • [{note.id}] {preview}")
    
    return "\n".join(lines)


@function_tool
def daily_summary() -> str:
    """
    Generate a summary of today's tasks and notes.
    
    Returns:
        Daily summary
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Pending tasks
    pending = [t for t in tasks if t.status == "pending"]
    due_today = [t for t in pending if t.due_date == today]
    high_priority = [t for t in pending if t.priority == "high"]
    
    # Completed today
    completed_today = [t for t in tasks if t.status == "completed"]
    
    lines = [
        f"📅 Daily Summary - {today}",
        "",
        f"📊 Overview:",
        f"  • Pending tasks: {len(pending)}",
        f"  • Due today: {len(due_today)}",
        f"  • High priority: {len(high_priority)}",
        f"  • Completed: {len(completed_today)}",
    ]
    
    if due_today:
        lines.append("\n🔔 Due Today:")
        for task in due_today:
            lines.append(f"  • {task.title}")
    
    if high_priority:
        lines.append("\n🔴 High Priority:")
        for task in high_priority:
            lines.append(f"  • {task.title}")
    
    return "\n".join(lines)


# ============================================
# Agent Definition
# ============================================

assistant_agent = Agent(
    name="Personal Assistant",
    instructions="""You are a helpful personal assistant. Help users manage their:
    
    1. Tasks - Add, complete, and organize tasks
    2. Notes - Take quick notes
    3. Daily planning - Provide summaries and priorities
    
    Be proactive:
    - Suggest priorities when asked about tasks
    - Remind about due dates
    - Offer to help organize when things get cluttered
    
    Be conversational but efficient. Use the available tools to help users.""",
    tools=[add_task, complete_task, list_tasks, take_note, list_notes, daily_summary],
)


async def chat(message: str) -> str:
    """Process a message through the assistant."""
    result = await Runner.run(assistant_agent, message)
    return result.final_output


async def main():
    """Interactive demo of the personal assistant."""
    load_data()
    
    print("="*50)
    print("🤖 PERSONAL ASSISTANT AGENT")
    print("="*50)
    print("Type 'quit' to exit\n")
    
    # Demo conversation
    demo_messages = [
        "Add a task: Review quarterly report, due 2026-01-15, high priority",
        "Add a task: Send follow-up emails, medium priority",
        "Add a task: Book team lunch, low priority",
        "Show me my tasks",
        "Give me today's summary",
        "Take a note: Remember to update the documentation",
    ]
    
    for message in demo_messages:
        print(f"\n👤 You: {message}")
        response = await chat(message)
        print(f"🤖 Assistant: {response}")
    
    print("\n" + "="*50)
    print("Demo complete! Data saved to assistant_data.json")


if __name__ == "__main__":
    asyncio.run(main())
