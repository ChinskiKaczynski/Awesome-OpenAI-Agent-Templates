# Customer Support Agent

An AI agent that handles customer support tickets with intelligent routing and response generation.

## Features

- 🎫 **Ticket Handling**: Process support tickets automatically
- 🔀 **Smart Routing**: Route to appropriate department (billing, technical, general)
- 💬 **Response Generation**: Create helpful, empathetic responses
- 📊 **Sentiment Analysis**: Detect customer emotions
- 📚 **Knowledge Base**: Reference FAQs and documentation

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

```
Support Ticket
      ↓
┌──────────────┐
│  Classifier  │ ← Determine type & urgency
└──────┬───────┘
       ↓
┌──────────────┐
│   Router     │ ← Route to specialist
└──────┬───────┘
       │
   ┌───┴───┐
   ↓       ↓
Billing  Technical
   ↓       ↓
   └───┬───┘
       ↓
┌──────────────┐
│  Responder   │ ← Generate response
└──────────────┘
```

## Response Template

```
Subject: Re: [Ticket ID]

Hi [Name],

[Empathetic acknowledgment]

[Solution/Next steps]

[Closing]

Best regards,
Support Team
```
