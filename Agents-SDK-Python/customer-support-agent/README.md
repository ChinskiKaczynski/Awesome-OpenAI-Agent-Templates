# Customer Support Agent

An AI agent that handles customer support tickets with intelligent routing and response generation.

## Features

- 🎫 **Ticket Handling**: Read sample support tickets
- 🔀 **Smart Routing**: Let the triage agent hand off to billing, technical, or general support
- 💬 **Response Generation**: Draft replies and print them to the console

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Example Tickets

```
"I've been charged twice for my subscription this month"
"The app crashes when I try to upload photos"
"How do I cancel my account?"
"Your service is amazing, thank you!"
```

## How It Works

The triage agent can hand off to a billing, technical, or general support agent using the Agents SDK. A handoff is model-selected, not guaranteed; the triage agent may answer directly.

```text
Support ticket
      |
      v
Support Triage
      |
      +--> Billing Specialist
      +--> Technical Support Specialist
      +--> General Support Agent
      |
      v
Draft reply printed to console
```

This is a response-drafting demo, not a ticketing integration: it does not classify or store ticket categories/urgency, perform sentiment analysis, search a knowledge base, send emails, issue refunds, or change customer accounts.

See the [Agents SDK handoffs guide](https://openai.github.io/openai-agents-python/handoffs/) for the routing mechanism.

## Illustrative Response Format

The example below is not enforced by the code.

```
Subject: Re: [Ticket ID]

Hi [Name],

[Empathetic acknowledgment]

[Solution/Next steps]

[Closing]

Best regards,
Support Team
```
