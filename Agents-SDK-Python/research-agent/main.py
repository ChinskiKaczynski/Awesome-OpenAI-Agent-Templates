"""
Research Agent
An AI agent that searches for information and synthesizes it into comprehensive reports.

Uses the Responses API with web_search built-in tool for real-time information.
"""
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlsplit

load_dotenv()

client = None


def get_client():
    """Initialize the API client only when research is requested."""
    global client
    if client is None:
        client = OpenAI()
    return client


class ResearchAgent:
    """Agent that conducts research and generates reports."""
    
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model
        self.research_results = []
        self.source_urls = []
        self.last_search_urls = []
    
    def search(self, query: str) -> str:
        """Search the web for information."""
        print(f"  🔍 Searching: {query}")
        self.last_search_urls = []
        
        response = get_client().responses.create(
            model=self.model,
            input=f"Search for: {query}. Provide detailed findings with sources.",
            tools=[{"type": "web_search"}],
            tool_choice="required"
        )

        # One successful search does not excuse a failed call or incomplete response.
        search_calls = [item for item in response.output if item.type == "web_search_call"]
        if (
            response.status != "completed"
            or not search_calls
            or any(item.status != "completed" for item in search_calls)
        ):
            raise RuntimeError("Web search did not complete; refusing to use unverified findings.")
        if not response.output_text or not response.output_text.strip():
            raise RuntimeError("Web search returned no findings; refusing to synthesize.")

        # Collect citations for this search before accepting its findings.
        cited_urls = []
        for item in response.output:
            if item.type == "message":
                for part in item.content:
                    if part.type == "output_text":
                        for annotation in part.annotations:
                            if annotation.type == "url_citation":
                                url = annotation.url
                                try:
                                    parsed = urlsplit(url)
                                    _ = parsed.port  # Reject malformed ports.
                                    valid = (
                                        parsed.scheme in ("http", "https")
                                        and bool(parsed.hostname)
                                        and not any(char.isspace() for char in url)
                                    )
                                except (TypeError, ValueError):
                                    valid = False
                                if valid and url not in cited_urls:
                                    cited_urls.append(url)

        if not cited_urls:
            raise RuntimeError("Web search returned no cited source URLs; refusing to synthesize unsupported findings.")
        self.last_search_urls = cited_urls
        for url in cited_urls:
            if url not in self.source_urls:
                self.source_urls.append(url)

        return response.output_text
    
    def plan_research(self, topic: str) -> list[str]:
        """Break down the topic into sub-questions."""
        print(f"📋 Planning research for: {topic}")
        
        response = get_client().responses.create(
            model=self.model,
            input=f"""You are a research planner. Break down this topic into 3-4 specific 
            sub-questions that would help create a comprehensive understanding.
            
            Topic: {topic}
            
            Return just the questions, one per line, no numbering."""
        )
        
        if response.status != "completed":
            raise RuntimeError("Research plan did not complete; refusing to use a partial plan.")
        if not response.output_text:
            return []
        questions = [q.strip() for q in response.output_text.split('\n') if q.strip()]
        return questions[:4]  # Limit to 4 sub-questions
    
    def synthesize(self, topic: str, findings: list[str]) -> str:
        """Synthesize findings into a report."""
        print("📝 Synthesizing findings...")
        
        findings_text = "\n\n---\n\n".join(findings)
        
        response = get_client().responses.create(
            model=self.model,
            input=f"""You are a research synthesizer. Create a comprehensive report from these findings.
            
            Topic: {topic}
            Date: {datetime.now().strftime("%Y-%m-%d")}
            
            Findings:
            {findings_text}
            
            Create a report with:
            1. Executive Summary (2-3 sentences)
            2. Key Findings (bullet points)
            3. Detailed Analysis (organized by theme)

            Do not invent citations or a Sources section; source URLs are appended
            separately from web search API annotations.
            Use markdown formatting."""
        )
        
        if response.status != "completed" or not response.output_text or not response.output_text.strip():
            raise RuntimeError("Report synthesis did not complete; refusing to publish an incomplete report.")
        return response.output_text
    
    def research(self, topic: str) -> str:
        """Conduct full research on a topic."""
        self.source_urls = []
        print(f"\n{'='*50}")
        print(f"🔬 Starting Research: {topic}")
        print(f"{'='*50}\n")
        
        # Step 1: Plan research
        questions = self.plan_research(topic)
        if not questions:
            raise RuntimeError("Research plan produced no questions; refusing to synthesize without web search.")
        print(f"  Questions to explore: {len(questions)}")
        for q in questions:
            print(f"    • {q}")
        print()
        
        # Step 2: Research each question
        findings = []
        evidence = []
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] Researching...")
            result = self.search(question)
            findings.append(f"## {question}\n\n{result}")
            evidence.append(
                f"### {question}\n\n{result}\n\nCited URLs for this search:\n"
                + "\n".join(f"- <{url}>" for url in self.last_search_urls)
            )
        
        # Step 3: Synthesize
        print()
        report = self.synthesize(topic, findings)
        if self.source_urls:
            report += "\n\n## Sources cited by web search\n\n" + "\n".join(
                f"- <{url}>" for url in self.source_urls
            )
        else:
            report += "\n\n> No source URLs were returned by web search; verify claims independently."

        report += "\n\n## Original search findings and citations\n\n" + "\n\n".join(evidence)
        return report


def main():
    """Run research only when an explicit topic is supplied."""
    import sys

    topic = " ".join(sys.argv[1:]).strip()
    if not topic:
        print('Usage: python main.py "research topic"')
        return

    agent = ResearchAgent()
    report = agent.research(topic)

    print(f"\n{'='*50}")
    print("📄 FINAL REPORT")
    print(f"{'='*50}\n")
    print(report)

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✅ Report saved to: {filename}")


if __name__ == "__main__":
    main()
