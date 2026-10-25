"""Offline citation provenance checks; no network or paid API calls."""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace as Obj
from unittest import TestCase, main, mock


def response(text, urls=(), search_status="completed", response_status="completed"):
    annotations = [Obj(type="url_citation", url=url) for url in urls]
    annotations.append(Obj(type="file_citation", url="https://ignored.example"))
    return Obj(status=response_status, output_text=text, output=[Obj(type="web_search_call", status=search_status), Obj(type="message", content=[
        Obj(type="output_text", annotations=annotations), Obj(type="refusal")
    ])])


class ResearchSourcesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        with mock.patch.dict(sys.modules, {
            "openai": Obj(OpenAI=mock.Mock(return_value=mock.Mock())),
            "dotenv": Obj(load_dotenv=lambda: None),
        }):
            spec = importlib.util.spec_from_file_location("research_agent_main", Path(__file__).with_name("main.py"))
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def setUp(self):
        self.client = mock.Mock()
        self.module.client = self.client
        self.agent = self.module.ResearchAgent()

    def test_search_collects_only_unique_url_citations(self):
        self.client.responses.create.return_value = response("Answer", ["https://source.example/a", "https://source.example/a", "http://source.example/b"])
        self.assertEqual(self.agent.search("query"), "Answer")
        self.assertEqual(self.agent.source_urls, ["https://source.example/a", "http://source.example/b"])
        self.assertEqual(self.client.responses.create.call_args.kwargs["tools"], [{"type": "web_search"}])
        self.assertEqual(self.client.responses.create.call_args.kwargs["tool_choice"], "required")

    def test_research_appends_api_sources_and_resets_between_runs(self):
        self.client.responses.create.side_effect = [
            response("Question?"), response("Found", ["https://source.example/a"]), response("Summary"),
            response("Question?"), response("Found", []), response("Summary 2")
        ]
        first = self.agent.research("Topic")
        self.assertIn("## Sources cited by web search\n\n- <https://source.example/a>", first)
        second = self.agent.research("Other topic")
        self.assertNotIn("https://source.example/a", second)
        self.assertIn("No source URLs were returned", second)
        self.assertIn("Do not invent citations", self.client.responses.create.call_args.kwargs["input"])


    def test_research_rejects_empty_plan_without_synthesizing(self):
        self.client.responses.create.return_value = response("  \n")
        with self.assertRaisesRegex(RuntimeError, "Research plan produced no questions"):
            self.agent.research("Topic")
        self.assertEqual(self.client.responses.create.call_count, 1)

    def test_search_rejects_missing_or_incomplete_web_search(self):
        for status in ("in_progress", "failed"):
            with self.subTest(status=status):
                self.client.responses.create.return_value = response("Unsourced answer", search_status=status)
                with self.assertRaisesRegex(RuntimeError, "Web search did not complete"):
                    self.agent.search("query")

        self.client.responses.create.return_value = Obj(
            status="completed", output_text="Unsourced answer", output=[Obj(type="message", content=[])]
        )
        with self.assertRaisesRegex(RuntimeError, "Web search did not complete"):
            self.agent.search("query")


    def test_search_rejects_partial_search_failure_or_incomplete_response(self):
        mixed = response("Partial findings", ["https://source.example/partial"])
        mixed.output.insert(1, Obj(type="web_search_call", status="failed"))
        for result in (mixed, response("Partial findings", response_status="incomplete")):
            with self.subTest(result=result):
                self.client.responses.create.return_value = result
                with self.assertRaisesRegex(RuntimeError, "Web search did not complete"):
                    self.agent.search("query")
                self.assertEqual(self.agent.source_urls, [])


    def test_real_openai_sdk_with_mock_http_transport(self):
        """Exercise SDK request serialization and typed response parsing offline."""
        import json

        from openai import OpenAI
        try:
            import httpx2 as httpx  # OpenAI SDK 3.x transport
        except ImportError:
            import httpx  # OpenAI SDK 2.x transport

        requests = []

        def respond(request):
            requests.append((request.url.path, json.loads(request.content)))
            return httpx.Response(200, json={
                "id": "resp_test",
                "object": "response",
                "created_at": 1,
                "model": "gpt-4.1-mini",
                "status": "completed",
                "parallel_tool_calls": True,
                "tool_choice": "required",
                "tools": [{"type": "web_search"}],
                "output": [
                    {
                        "id": "ws_test",
                        "type": "web_search_call",
                        "status": "completed",
                        "action": {"type": "search", "query": "query"},
                    },
                    {
                        "id": "msg_test",
                        "type": "message",
                        "role": "assistant",
                        "status": "completed",
                        "content": [{
                            "type": "output_text",
                            "text": "Answer",
                            "annotations": [{
                                "type": "url_citation",
                                "url": "https://example.org/source",
                                "title": "Example",
                                "start_index": 0,
                                "end_index": 6,
                            }],
                        }],
                    },
                ],
            })

        with httpx.Client(transport=httpx.MockTransport(respond)) as http_client:
            self.module.client = OpenAI(api_key="sk-test", http_client=http_client)
            self.assertEqual(self.agent.search("query"), "Answer")
        self.assertEqual(self.agent.source_urls, ["https://example.org/source"])
        self.assertEqual(len(requests), 1)
        path, payload = requests[0]
        self.assertEqual(path, "/v1/responses")
        self.assertEqual(payload["tools"], [{"type": "web_search"}])
        self.assertEqual(payload["tool_choice"], "required")



if __name__ == "__main__":
    main()
