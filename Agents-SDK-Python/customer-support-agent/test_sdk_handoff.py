"""Exercise the real Agents SDK handoff loop with a scripted model (no API calls)."""
import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from agents import RunConfig
from agents.testing import ScriptedModel, assistant_message, function_call


class SupportSdkHandoffTests(unittest.IsolatedAsyncioTestCase):
    async def test_ticket_routes_to_billing_with_real_runner(self):
        spec = importlib.util.spec_from_file_location(
            "support_sdk_handoff_demo", Path(__file__).with_name("main.py")
        )
        demo = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = demo
        try:
            spec.loader.exec_module(demo)
            model = ScriptedModel([
                [function_call("transfer_to_billing_specialist", {}, call_id="handoff_1")],
                [assistant_message("Please contact the billing support team.")],
            ])
            ticket = demo.Ticket(
                id="T-OFFLINE", customer_name="Private Person",
                email="private@example.test", message="Confidential billing question",
            )

            def offline_config(**kwargs):
                self.assertIs(kwargs.get("trace_include_sensitive_data"), False)
                return RunConfig(model=model, tracing_disabled=True, **kwargs)

            stdout = io.StringIO()
            with patch.object(demo, "RunConfig", side_effect=offline_config):
                with contextlib.redirect_stdout(stdout):
                    answer = await demo.handle_ticket(ticket)

            self.assertEqual(answer, "Please contact the billing support team.")
            self.assertIn("Routed to: Billing Specialist", stdout.getvalue())
            self.assertNotIn(ticket.email, stdout.getvalue())
            self.assertNotIn(ticket.message, stdout.getvalue())
            self.assertEqual(len(model.calls), 2)
            self.assertEqual(model.first_call.model_settings.tool_choice, "required")
            model.assert_complete()
        finally:
            sys.modules.pop(spec.name, None)


if __name__ == "__main__":
    unittest.main()
