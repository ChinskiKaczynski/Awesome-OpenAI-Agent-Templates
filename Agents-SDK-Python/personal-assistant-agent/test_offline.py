"""Offline regression tests for the personal assistant's task logic and CLI.

The Agents SDK is stubbed only at the import boundary; no model or API calls.
"""
import asyncio
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


def load_example():
    sdk = types.ModuleType("agents")

    class FakeRunner:
        calls = []

        @classmethod
        async def run(cls, agent, message, session=None):
            cls.calls.append((agent, message, session))
            return types.SimpleNamespace(final_output="Mock response")

    class FakeSQLiteSession:
        def __init__(self, session_id):
            self.session_id = session_id

    sdk.Agent = lambda **kwargs: types.SimpleNamespace(**kwargs)
    sdk.Runner = FakeRunner
    sdk.SQLiteSession = FakeSQLiteSession
    sdk.function_tool = lambda fn: fn

    name = "personal_assistant_offline_fixture"
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).with_name("main.py")
    )
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"agents": sdk, name: module}):
        spec.loader.exec_module(module)
    return module, FakeRunner, FakeSQLiteSession


class PersonalAssistantOfflineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.example, self.runner, self.session_type = load_example()
        self.example.DATA_FILE = Path(self.tmp.name) / "assistant_data.json"

    def test_completion_is_persisted_and_idempotent(self):
        task = self.example.Task(id="task_1", title="Check backup")
        self.example.tasks.append(task)
        first = self.example.complete_task("task_1")
        completed_at = task.completed_at
        self.assertIn("Completed", first)
        self.assertTrue(completed_at)
        self.assertIn("already completed", self.example.complete_task("task_1"))
        self.assertEqual(task.completed_at, completed_at)
        self.assertEqual(
            __import__("json").loads(self.example.DATA_FILE.read_text())["tasks"][0]["completed_at"],
            completed_at,
        )

    def test_daily_summary_counts_only_completions_from_today(self):
        from datetime import datetime, timedelta
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        self.example.tasks.extend([
            self.example.Task("1", "Today", status="completed", completed_at=f"{today}T10:00:00"),
            self.example.Task("2", "Yesterday", status="completed", completed_at=f"{yesterday}T10:00:00"),
            self.example.Task("3", "Legacy", status="completed", completed_at=None),
            self.example.Task("4", "Pending", status="pending", due_date=str(today), priority="high"),
        ])
        summary = self.example.daily_summary()
        self.assertIn("Completed today: 1", summary)
        self.assertIn("Pending tasks: 1", summary)
        self.assertIn("Due today: 1", summary)
        self.assertIn("High priority: 1", summary)

    def test_chat_passes_same_session_to_runner(self):
        session = self.session_type("local-test")
        result = asyncio.run(self.example.chat("List my tasks", session))
        self.assertEqual(result, "Mock response")
        self.assertEqual(len(self.runner.calls), 1)
        agent, message, received_session = self.runner.calls[0]
        self.assertIs(agent, self.example.assistant_agent)
        self.assertEqual(message, "List my tasks")
        self.assertIs(received_session, session)

    def test_quit_does_not_seed_tasks_or_call_model(self):
        with patch("builtins.input", return_value="quit"):
            asyncio.run(self.example.main())
        self.assertEqual(self.example.tasks, [])
        self.assertEqual(self.runner.calls, [])
        self.assertFalse(self.example.DATA_FILE.exists())


if __name__ == "__main__":
    unittest.main()
