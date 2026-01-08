"""
Agents as Tools Pattern
Use agents as tools for other agents, enabling modular composition.

This pattern allows you to build complex workflows by composing
specialized agents together.
"""
import asyncio
from agents import Agent, Runner, function_tool


# ============================================
# Specialist Agents (will be used as tools)
# ============================================

research_agent = Agent(
    name="Research Agent",
    instructions="""You are a research specialist. When given a topic:
    1. Identify key concepts and facts
    2. Find relevant data and statistics
    3. Return a structured summary of findings
    
    Be thorough but concise. Focus on accuracy and relevance.""",
)

writer_agent = Agent(
    name="Writer Agent",
    instructions="""You are a professional writer. When given content:
    1. Structure it clearly with introduction, body, conclusion
    2. Make it engaging and readable
    3. Maintain a professional yet approachable tone
    
    Focus on clarity and flow.""",
)

editor_agent = Agent(
    name="Editor Agent",
    instructions="""You are a meticulous editor. When given text:
    1. Check for grammar and spelling
    2. Improve clarity and conciseness
    3. Ensure consistent tone and style
    
    Return the polished version.""",
)


# ============================================
# Tool Functions (wrap agents as tools)
# ============================================

@function_tool
async def research_topic(topic: str) -> str:
    """
    Research a topic and return key findings.
    
    Args:
        topic: The topic to research
    
    Returns:
        Research findings summary
    """
    result = await Runner.run(research_agent, f"Research this topic: {topic}")
    return result.final_output


@function_tool
async def write_content(content_brief: str) -> str:
    """
    Write content based on a brief.
    
    Args:
        content_brief: What to write and key points to include
    
    Returns:
        Written content
    """
    result = await Runner.run(writer_agent, f"Write based on this brief: {content_brief}")
    return result.final_output


@function_tool
async def edit_text(text: str) -> str:
    """
    Edit and polish text.
    
    Args:
        text: The text to edit
    
    Returns:
        Edited text
    """
    result = await Runner.run(editor_agent, f"Edit this text: {text}")
    return result.final_output


# ============================================
# Orchestrator Agent
# ============================================

orchestrator_agent = Agent(
    name="Content Orchestrator",
    instructions="""You are a content orchestrator. Your job is to coordinate
    the creation of high-quality content by using your specialist tools:
    
    1. Use research_topic to gather information
    2. Use write_content to create the initial draft
    3. Use edit_text to polish the final version
    
    Always use all three tools in sequence for best results.
    Return the final polished content to the user.""",
    tools=[research_topic, write_content, edit_text],
)


async def main():
    """Demo the agents-as-tools pattern."""
    
    request = "Create a short blog post about the benefits of meditation"
    
    print(f"👤 User Request: {request}")
    print("=" * 50)
    print("🔄 Orchestrator coordinating work...\n")
    
    result = await Runner.run(orchestrator_agent, request)
    
    print("=" * 50)
    print(f"📝 Final Output:\n{result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
