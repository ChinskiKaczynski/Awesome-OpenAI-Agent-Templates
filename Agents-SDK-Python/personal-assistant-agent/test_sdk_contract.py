"""Exercise the real Agents SDK function-tool boundary without an API call.

Unlike test_offline.py, this module deliberately does NOT stub the agents package.
"""
import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from agents import FunctionTool, RunContextWrapper


def load_real_example():
    path = Path(__file__).with_name("main.py")
    name = "personal_assistant_real_sdk_contract"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class RealSDKToolContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_registered_tools_invoke_and_persist_locally(self):
        example = load_real_example()
        self.assertEqual(
            {tool.name for tool in example.assistant_agent.tools},
            {"add_task", "complete_task", "list_tasks", "take_note", "list_notes", "daily_summary"},
        )
        self.assertTrue(all(isinstance(tool, FunctionTool) for tool in example.assistant_agent.tools))
        context = RunContextWrapper(context=None)
        with tempfile.TemporaryDirectory() as directory:
            example.DATA_FILE = Path(directory) / "assistant_data.json"
            self.assertFalse(example.DATA_FILE.exists())
            added = await example.add_task.on_invoke_tool(
                context, json.dumps({"title": "Check backup", "priority": "high"})
            )
            self.assertIn("Added task", str(added))
            saved = json.loads(example.DATA_FILE.read_text(encoding="utf-8"))
            self.assertEqual(saved["tasks"][0]["title"], "Check backup")

            completed = await example.complete_task.on_invoke_tool(
                context, json.dumps({"task_id": "task_1"})
            )
            self.assertIn("Completed", str(completed))
            saved = json.loads(example.DATA_FILE.read_text(encoding="utf-8"))
            self.assertEqual(saved["tasks"][0]["status"], "completed")
            self.assertIsNotNone(saved["tasks"][0]["completed_at"])

            summary = await example.daily_summary.on_invoke_tool(context, "{}")
            self.assertIn("Completed today: 1", str(summary))


if __name__ == "__main__":
    unittest.main()
