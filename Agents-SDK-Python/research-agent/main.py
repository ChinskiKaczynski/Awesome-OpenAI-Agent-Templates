"""
Research Agent
An AI agent that searches for information and synthesizes it into comprehensive reports.

Uses the Responses API with web_search built-in tool for real-time information.
"""
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = OpenAI()


class ResearchAgent:
    """Agent that conducts research and generates reports."""
    
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model
        self.research_results = []
        self.source_urls = []
    
    def search(self, query: str) -> str:
        """Search the web for information."""
        print(f"  🔍 Searching: {query}")
        
        response = client.responses.create(
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

        # Retain citation URLs supplied by the API, rather than inferred by synthesis.
        for item in response.output:
            if item.type == "message":
                for part in item.content:
                    if part.type == "output_text":
                        for annotation in part.annotations:
                            if annotation.type == "url_citation":
                                url = annotation.url
                                if url.startswith(("https://", "http://")) and url not in self.source_urls:
                                    self.source_urls.append(url)

        return response.output_text
    
    def plan_research(self, topic: str) -> list[str]:
        """Break down the topic into sub-questions."""
        print(f"📋 Planning research for: {topic}")
        
        response = client.responses.create(
            model=self.model,
            input=f"""You are a research planner. Break down this topic into 3-4 specific 
            sub-questions that would help create a comprehensive understanding.
            
            Topic: {topic}
            
            Return just the questions, one per line, no numbering."""
        )
        
        questions = [q.strip() for q in response.output_text.strip().split('\n') if q.strip()]
        return questions[:4]  # Limit to 4 sub-questions
    
    def synthesize(self, topic: str, findings: list[str]) -> str:
        """Synthesize findings into a report."""
        print("📝 Synthesizing findings...")
        
        findings_text = "\n\n---\n\n".join(findings)
        
        response = client.responses.create(
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
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] Researching...")
            result = self.search(question)
            findings.append(f"## {question}\n\n{result}")
        
        # Step 3: Synthesize
        print()
        report = self.synthesize(topic, findings)
        if self.source_urls:
            report += "\n\n## Sources cited by web search\n\n" + "\n".join(
                f"- <{url}>" for url in self.source_urls
            )
        else:
            report += "\n\n> No source URLs were returned by web search; verify claims independently."

        return report


def main():
    """Demo the research agent."""
    agent = ResearchAgent()
    
    topics = [
        "What are the latest breakthroughs in quantum computing in 2025?",
    ]
    
    for topic in topics:
        report = agent.research(topic)
        
        print(f"\n{'='*50}")
        print("📄 FINAL REPORT")
        print(f"{'='*50}\n")
        print(report)
        
        # Save report
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ Report saved to: {filename}")


if __name__ == "__main__":
    main()
