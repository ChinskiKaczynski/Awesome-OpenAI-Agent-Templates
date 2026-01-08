"""
Customer Support Agent
An AI agent that handles customer support tickets with intelligent routing.

Uses the Agents SDK for multi-agent handoffs.
"""
import asyncio
from dataclasses import dataclass
from enum import Enum
from agents import Agent, Runner


class TicketCategory(Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"
    FEEDBACK = "feedback"


class Urgency(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Ticket:
    """Support ticket data structure."""
    id: str
    customer_name: str
    email: str
    message: str
    category: TicketCategory = None
    urgency: Urgency = None


# ============================================
# Specialist Agents
# ============================================

billing_agent = Agent(
    name="Billing Specialist",
    instructions="""You are a billing support specialist. Handle:
    - Payment issues and refunds
    - Subscription changes
    - Invoice questions
    - Pricing inquiries
    
    Always:
    1. Acknowledge the customer's concern
    2. Explain the situation clearly
    3. Provide actionable next steps
    4. Offer additional help
    
    Be empathetic and solution-focused. If you need to process a refund
    or make account changes, explain what you'll do and the timeline.""",
)

technical_agent = Agent(
    name="Technical Support Specialist",
    instructions="""You are a technical support specialist. Handle:
    - Bug reports
    - App crashes and errors
    - Feature questions
    - Integration issues
    
    Always:
    1. Acknowledge the frustration
    2. Ask clarifying questions if needed
    3. Provide step-by-step solutions
    4. Offer to escalate if unresolved
    
    Be patient and thorough. Use clear, non-technical language.""",
)

general_agent = Agent(
    name="General Support Agent",
    instructions="""You are a general support agent. Handle:
    - Account questions
    - General inquiries
    - Feedback and suggestions
    - Process guidance
    
    Be helpful, friendly, and professional. Guide customers
    to the right resources or information.""",
)

# Triage agent that routes to specialists
triage_agent = Agent(
    name="Support Triage",
    instructions="""You are a support triage agent. Analyze incoming tickets and:
    
    1. Determine the category:
       - BILLING: payments, subscriptions, invoices, pricing
       - TECHNICAL: bugs, errors, crashes, features, integrations
       - GENERAL: everything else
    
    2. Assess urgency:
       - CRITICAL: service down, data loss, security issues
       - HIGH: can't use core features, payment problems
       - MEDIUM: inconvenience, questions
       - LOW: feedback, suggestions
    
    3. Briefly acknowledge the customer, then hand off to the appropriate specialist.
    
    Example: "Thanks for reaching out! I'm connecting you with our billing team."
    """,
    handoffs=[billing_agent, technical_agent, general_agent],
)


async def handle_ticket(ticket: Ticket) -> str:
    """Process a support ticket through the agent system."""
    print(f"\n{'='*50}")
    print(f"🎫 Ticket #{ticket.id}")
    print(f"👤 From: {ticket.customer_name} <{ticket.email}>")
    print(f"{'='*50}")
    print(f"📝 Message:\n{ticket.message}")
    print(f"{'='*50}\n")
    
    # Format ticket for agent
    agent_input = f"""
    Customer: {ticket.customer_name}
    Email: {ticket.email}
    
    Message:
    {ticket.message}
    """
    
    # Process through triage
    result = await Runner.run(triage_agent, agent_input)
    
    print(f"🔀 Routed to: {result.last_agent.name}")
    print(f"\n📧 Response:\n{result.final_output}")
    
    return result.final_output


async def main():
    """Demo the customer support agent with sample tickets."""
    
    tickets = [
        Ticket(
            id="T-001",
            customer_name="John Smith",
            email="john@example.com",
            message="I was charged twice for my subscription this month. "
                    "Please refund the duplicate charge. Order #12345."
        ),
        Ticket(
            id="T-002",
            customer_name="Sarah Johnson",
            email="sarah@example.com",
            message="The mobile app keeps crashing whenever I try to upload "
                    "a photo. I'm using iPhone 15 with iOS 17. This started "
                    "after the last update."
        ),
        Ticket(
            id="T-003",
            customer_name="Mike Brown",
            email="mike@example.com",
            message="How do I export my data? I need a backup of everything."
        ),
        Ticket(
            id="T-004",
            customer_name="Emily Davis",
            email="emily@example.com",
            message="Just wanted to say your product is fantastic! The new "
                    "dark mode feature is exactly what I needed. Great work team!"
        ),
    ]
    
    for ticket in tickets:
        await handle_ticket(ticket)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
