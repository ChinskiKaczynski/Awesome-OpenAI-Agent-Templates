"""
Parallel Agents Pattern
Run multiple agents concurrently and aggregate results.

This pattern is useful when you need to perform independent
analysis or queries that can run in parallel.
"""
import asyncio
from agents import Agent, Runner


# ============================================
# Parallel Analysis Agents
# ============================================

sentiment_agent = Agent(
    name="Sentiment Analyzer",
    instructions="""Analyze the sentiment of the given text.
    
    Return a JSON object with:
    - sentiment: "positive", "negative", or "neutral"
    - confidence: 0.0 to 1.0
    - key_phrases: list of phrases that influenced your analysis
    
    Be precise and objective.""",
)

topic_agent = Agent(
    name="Topic Extractor",
    instructions="""Extract the main topics from the given text.
    
    Return a JSON object with:
    - main_topic: primary subject
    - subtopics: list of secondary topics
    - keywords: important terms
    
    Focus on substance, not style.""",
)

summary_agent = Agent(
    name="Summarizer",
    instructions="""Create a concise summary of the given text.
    
    Return a JSON object with:
    - one_sentence: single sentence summary
    - key_points: list of 3-5 main points
    - word_count: original text word count
    
    Be concise but complete.""",
)


# ============================================
# Parallel Execution
# ============================================

async def analyze_in_parallel(text: str) -> dict:
    """
    Run all analysis agents in parallel and collect results.
    
    Args:
        text: The text to analyze
    
    Returns:
        Dictionary with results from all agents
    """
    print("🔄 Running agents in parallel...")
    
    # Create tasks for parallel execution
    tasks = [
        Runner.run(sentiment_agent, text),
        Runner.run(topic_agent, text),
        Runner.run(summary_agent, text),
    ]
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Aggregate results
    return {
        "sentiment": results[0].final_output,
        "topics": results[1].final_output,
        "summary": results[2].final_output,
    }


# ============================================
# Aggregator Agent (optional)
# ============================================

aggregator_agent = Agent(
    name="Result Aggregator",
    instructions="""You receive analysis results from multiple specialists.
    Your job is to synthesize these into a unified report.
    
    Create a clear, structured summary that combines:
    - Sentiment insights
    - Topic coverage
    - Key takeaways
    
    Make it actionable and easy to understand.""",
)


async def analyze_with_aggregation(text: str) -> str:
    """
    Run parallel analysis and then aggregate results.
    """
    # Run parallel analysis
    parallel_results = await analyze_in_parallel(text)
    
    # Create aggregation prompt
    aggregation_prompt = f"""
    Please synthesize these analysis results into a unified report:
    
    SENTIMENT ANALYSIS:
    {parallel_results['sentiment']}
    
    TOPIC EXTRACTION:
    {parallel_results['topics']}
    
    SUMMARY:
    {parallel_results['summary']}
    """
    
    print("📊 Aggregating results...")
    final_result = await Runner.run(aggregator_agent, aggregation_prompt)
    
    return final_result.final_output


async def main():
    """Demo the parallel agents pattern."""
    
    sample_text = """
    Artificial intelligence is transforming the healthcare industry in remarkable ways.
    Machine learning algorithms can now detect diseases earlier than ever before,
    analyzing medical images with accuracy that rivals or exceeds human experts.
    However, concerns about data privacy and algorithmic bias must be addressed.
    Despite these challenges, the potential benefits for patient outcomes are substantial,
    and many hospitals are rapidly adopting AI-powered diagnostic tools.
    """
    
    print("📝 Input Text:")
    print(sample_text)
    print("=" * 50)
    
    # Option 1: Just parallel results
    # results = await analyze_in_parallel(sample_text)
    # print("Results:", results)
    
    # Option 2: Parallel + aggregation
    final_report = await analyze_with_aggregation(sample_text)
    
    print("\n" + "=" * 50)
    print("📋 Final Aggregated Report:")
    print(final_report)


if __name__ == "__main__":
    asyncio.run(main())
