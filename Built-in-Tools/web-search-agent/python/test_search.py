"""Offline contract checks: no API key, no network, no billable calls."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace as Obj
import unittest
from unittest.mock import Mock, patch


def fake_response(*, status="completed", calls=("completed",), text="Answer [1]", cited=True, citation_url="https://example.org/source"):
    annotations = [Obj(type="url_citation", url=citation_url)] if cited else []
    return Obj(
        status=status,
        output_text=text,
        output=[
            *(Obj(type="web_search_call", status=call_status) for call_status in calls),
            Obj(type="message", content=[Obj(type="output_text", annotations=annotations)]),
        ],
    )


class WebSearchOfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client = Mock()
        with patch.dict(sys.modules, {
            "openai": Obj(OpenAI=lambda: cls.mock_client),
            "dotenv": Obj(load_dotenv=lambda: None),
        }):
            spec = importlib.util.spec_from_file_location("web_search_under_test", Path(__file__).with_name("main.py"))
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def setUp(self):
        self.mock_client.reset_mock()

    def test_completed_cited_search_is_returned(self):
        self.mock_client.responses.create.return_value = fake_response()
        self.assertEqual(self.module.search_web("question"), "Answer [1]")
        kwargs = self.mock_client.responses.create.call_args.kwargs
        self.assertEqual(kwargs["tools"], [{"type": "web_search"}])
        self.assertEqual(kwargs["tool_choice"], "required")
        self.assertEqual(kwargs["input"], "question")

    def test_incomplete_or_missing_search_is_rejected(self):
        for response in (
            fake_response(status="incomplete"),
            fake_response(calls=()),
            fake_response(calls=("failed",)),
            fake_response(calls=("completed", "failed")),
        ):
            with self.subTest(response=response):
                self.mock_client.responses.create.return_value = response
                with self.assertRaisesRegex(RuntimeError, "did not complete"):
                    self.module.search_web("question")

    def test_empty_or_uncited_answer_is_rejected(self):
        for response, expected in (
            (fake_response(text="  "), "empty answer"),
            (fake_response(cited=False), "no source citations"),
        ):
            with self.subTest(response=response):
                self.mock_client.responses.create.return_value = response
                with self.assertRaisesRegex(RuntimeError, expected):
                    self.module.search_web("question")


    def test_malformed_source_urls_are_rejected(self):
        for url in (
            None,
            "",
            "javascript:alert(1)",
            "https://",
            "https://bad domain.test",
            "https://example.org:99999/article",
        ):
            with self.subTest(url=url):
                self.mock_client.responses.create.return_value = fake_response(citation_url=url)
                with self.assertRaisesRegex(RuntimeError, "no source citations"):
                    self.module.search_web("question")

    def test_http_source_url_is_accepted(self):
        self.mock_client.responses.create.return_value = fake_response(citation_url="http://example.org/article")
        self.assertEqual(self.module.search_web("question"), "Answer [1]")


if __name__ == "__main__":
    unittest.main()
