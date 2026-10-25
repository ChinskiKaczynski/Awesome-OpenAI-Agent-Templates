"""Offline regression tests for the support demo; no SDK or API key needed."""
import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, patch


class SupportDemoTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        fake_sdk = ModuleType("agents")
        fake_sdk.Agent = lambda **kwargs: SimpleNamespace(**kwargs)
        fake_sdk.RunConfig = lambda **kwargs: SimpleNamespace(**kwargs)
        fake_sdk.Runner = SimpleNamespace(run=AsyncMock())
        with patch.dict(sys.modules, {"agents": fake_sdk}):
            spec = importlib.util.spec_from_file_location("support_demo_under_test", Path(__file__).with_name("main.py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            try:
                spec.loader.exec_module(module)
            finally:
                del sys.modules[spec.name]
        cls.demo = module

    async def test_ticket_reaches_triage_without_echoing_raw_input(self):
        ticket = self.demo.Ticket(
            id="T-123", customer_name="Private Person",
            email="private@example.test", message="Secret ticket details",
        )
        reply = "Please contact our support team."
        self.demo.Runner.run = AsyncMock(return_value=SimpleNamespace(
            last_agent=self.demo.billing_agent, final_output=reply,
        ))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            actual = await self.demo.handle_ticket(ticket)

        self.assertEqual(actual, reply)
        self.demo.Runner.run.assert_awaited_once()
        args, kwargs = self.demo.Runner.run.await_args
        self.assertIs(args[0], self.demo.triage_agent)
        for detail in (ticket.customer_name, ticket.email, ticket.message):
            self.assertIn(detail, args[1])
            self.assertNotIn(detail, stdout.getvalue())
        self.assertIs(kwargs["run_config"].trace_include_sensitive_data, False)
        self.assertIn("T-123", stdout.getvalue())
        self.assertIn("Billing Specialist", stdout.getvalue())
        self.assertIn(reply, stdout.getvalue())

    async def test_runner_failure_does_not_echo_ticket(self):
        ticket = self.demo.Ticket("T-456", "Private Person", "private@example.test", "Secret ticket details")
        self.demo.Runner.run = AsyncMock(side_effect=RuntimeError("Simulated failure"))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with self.assertRaisesRegex(RuntimeError, "Simulated failure"):
                await self.demo.handle_ticket(ticket)
        self.assertNotIn(ticket.email, stdout.getvalue())
        self.assertNotIn(ticket.message, stdout.getvalue())

    async def test_handoffs_and_billing_instruction_are_configured(self):
        self.assertEqual(
            [agent.name for agent in self.demo.triage_agent.handoffs],
            ["Billing Specialist", "Technical Support Specialist", "General Support Agent"],
        )
        instructions = self.demo.billing_agent.instructions
        self.assertIn("cannot access billing systems", instructions)
        self.assertIn("Never claim a refund was processed", instructions)


if __name__ == "__main__":
    unittest.main()
