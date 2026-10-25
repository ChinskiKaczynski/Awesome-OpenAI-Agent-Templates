"""Offline citation provenance checks; no network or paid API calls."""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace as Obj
from unittest import TestCase, main, mock


def response(text, urls=()):
    annotations = [Obj(type="url_citation", url=url) for url in urls]
    annotations.append(Obj(type="file_citation", url="https://ignored.example"))
    return Obj(output_text=text, output=[Obj(type="web_search_call"), Obj(type="message", content=[
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


if __name__ == "__main__":
    main()
