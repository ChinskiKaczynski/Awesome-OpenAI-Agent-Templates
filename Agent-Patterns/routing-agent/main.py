"""
Routing Agent Pattern
Route incoming requests to specialized agents based on intent.

Uses the OpenAI Agents SDK handoff feature for seamless transfer.
"""
import asyncio
from agents import Agent, Runner


# Define specialized agents
sales_agent = Agent(
    name="Sales Agent",
    instructions="""You are a sales specialist. Help customers with:
    - Pricing questions
    - Subscription upgrades/downgrades
    - Billing inquiries
    - Product comparisons
    
    Be friendly and solution-oriented. Always try to help the customer
    find the best plan for their needs.""",
)

tech_support_agent = Agent(
    name="Tech Support Agent",
    instructions="""You are a technical support specialist. Help customers with:
    - Bug reports and troubleshooting
    - Feature questions
    - Integration help
    - API documentation
    
    Be patient and thorough. Ask clarifying questions when needed.""",
)

general_agent = Agent(
    name="General Support Agent",
    instructions="""You are a general support agent. Help with:
    - General questions about the company
    - Account management
    - Feedback collection
    
    If the request is clearly sales or technical, inform that you'll
    transfer them to the right specialist.""",
)

# Triage agent - routes to specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a triage agent. Your job is to understand the customer's
    request and route them to the appropriate specialist:
    
    - Sales Agent: pricing, billing, subscriptions, upgrades
    - Tech Support Agent: bugs, errors, technical issues, integrations
    - General Agent: everything else
    
    Briefly acknowledge the customer's request before handing off.
    Example: "I'll connect you with our sales team for that."
    """,
    handoffs=[sales_agent, tech_support_agent, general_agent],
)


async def handle_request(user_message: str):
    """Process a user request through the routing system."""
    print(f"\n{'='*50}")
    print(f"👤 User: {user_message}")
    print(f"{'='*50}")
    
    result = await Runner.run(triage_agent, user_message)
    
    print(f"\n🤖 Final Agent: {result.last_agent.name}")
    print(f"📝 Response: {result.final_output}")
    
    return result


async def main():
    """Demo the routing agent with sample requests."""
    
    test_requests = [
        "I want to upgrade to the Pro plan",
        "My application keeps crashing when I try to upload files",
        "What are your business hours?",
        "How much does the enterprise tier cost?",
        "I'm getting a 500 error from your API",
    ]
    
    for request in test_requests:
        await handle_request(request)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
