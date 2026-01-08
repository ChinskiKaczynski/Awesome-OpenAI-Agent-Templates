"""
Content Writer Agent
An AI agent that writes high-quality content for various formats.

Supports blog posts, emails, social media, and marketing copy.
"""
from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import dataclass
from enum import Enum
from typing import Optional

load_dotenv()

client = OpenAI()


class ContentType(Enum):
    BLOG_POST = "blog_post"
    EMAIL_MARKETING = "email_marketing"
    EMAIL_PROFESSIONAL = "email_professional"
    SOCIAL_TWITTER = "social_twitter"
    SOCIAL_LINKEDIN = "social_linkedin"
    AD_COPY = "ad_copy"
    LANDING_PAGE = "landing_page"


class Tone(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    PERSUASIVE = "persuasive"
    INSPIRATIONAL = "inspirational"


@dataclass
class ContentRequest:
    """Content generation request."""
    topic: str
    content_type: ContentType
    tone: Tone = Tone.PROFESSIONAL
    length: str = "medium"  # short, medium, long
    keywords: list[str] = None
    audience: str = "general"
    additional_context: str = ""


CONTENT_TEMPLATES = {
    ContentType.BLOG_POST: """Write a {length} blog post about: {topic}

Tone: {tone}
Target audience: {audience}
{keywords_section}

Structure:
1. Compelling headline (use power words)
2. Hook paragraph (grab attention)
3. Main content with subheadings (H2, H3)
4. Practical examples or tips
5. Conclusion with call-to-action

Make it SEO-friendly and engaging.""",

    ContentType.EMAIL_MARKETING: """Write a marketing email about: {topic}

Tone: {tone}
Target audience: {audience}
{keywords_section}

Include:
1. Subject line (compelling, under 50 chars)
2. Preheader text
3. Opening hook
4. Value proposition
5. Clear CTA button text
6. P.S. line (optional but effective)

Make it scannable with short paragraphs.""",

    ContentType.EMAIL_PROFESSIONAL: """Write a professional email about: {topic}

Tone: {tone}
Context: {additional_context}

Include:
1. Clear subject line
2. Professional greeting
3. Purpose statement (first paragraph)
4. Supporting details
5. Clear next steps or ask
6. Professional sign-off

Keep it concise and actionable.""",

    ContentType.SOCIAL_TWITTER: """Write 5 tweet variations about: {topic}

Tone: {tone}
Target audience: {audience}
{keywords_section}

Requirements:
- Under 280 characters each
- Include relevant hashtags
- Make them engaging and shareable
- Vary the style (question, statement, statistic, etc.)""",

    ContentType.SOCIAL_LINKEDIN: """Write a LinkedIn post about: {topic}

Tone: {tone}
Target audience: {audience}

Structure:
1. Hook line (stops the scroll)
2. Personal insight or story
3. Key points (use line breaks)
4. Takeaway or lesson
5. Engagement question
6. Relevant hashtags (3-5)

Make it authentic and valuable.""",

    ContentType.AD_COPY: """Write ad copy for: {topic}

Tone: {tone}
Target audience: {audience}
{keywords_section}

Create:
1. 3 headline variations (max 30 chars)
2. 3 description variations (max 90 chars)
3. Display URL path suggestion
4. Call-to-action options

Focus on benefits, urgency, and differentiation.""",

    ContentType.LANDING_PAGE: """Write landing page copy for: {topic}

Tone: {tone}
Target audience: {audience}
{keywords_section}

Sections:
1. Hero headline + subheadline
2. Problem statement
3. Solution/product introduction
4. Key features (3-5 with benefits)
5. Social proof section idea
6. FAQ section (3-5 questions)
7. Final CTA section

Make it persuasive and scannable.""",
}


class ContentWriterAgent:
    """Agent that generates various types of content."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    
    def write(self, request: ContentRequest) -> str:
        """Generate content based on the request."""
        template = CONTENT_TEMPLATES[request.content_type]
        
        keywords_section = ""
        if request.keywords:
            keywords_section = f"Keywords to include: {', '.join(request.keywords)}"
        
        prompt = template.format(
            topic=request.topic,
            tone=request.tone.value,
            length=request.length,
            audience=request.audience,
            keywords_section=keywords_section,
            additional_context=request.additional_context or "N/A"
        )
        
        print(f"✍️  Generating {request.content_type.value}...")
        print(f"   Topic: {request.topic}")
        print(f"   Tone: {request.tone.value}")
        
        response = client.responses.create(
            model=self.model,
            input=prompt,
        )
        
        return response.output_text
    
    def rewrite(self, original: str, instructions: str) -> str:
        """Rewrite existing content with specific instructions."""
        print("🔄 Rewriting content...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Rewrite this content following these instructions:

INSTRUCTIONS: {instructions}

ORIGINAL CONTENT:
{original}

Provide the rewritten version:"""
        )
        
        return response.output_text
    
    def improve(self, content: str) -> str:
        """Suggest improvements for existing content."""
        print("🔍 Analyzing content for improvements...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Analyze this content and provide specific improvements:

CONTENT:
{content}

Provide:
1. Strengths (what works well)
2. Weaknesses (what needs improvement)
3. Specific suggestions (with examples)
4. Improved version of any weak sections"""
        )
        
        return response.output_text


def main():
    """Demo the content writer agent."""
    agent = ContentWriterAgent()
    
    print("="*50)
    print("✍️  CONTENT WRITER AGENT DEMO")
    print("="*50)
    
    # Demo 1: Blog Post
    print("\n\n--- BLOG POST ---\n")
    blog = agent.write(ContentRequest(
        topic="The Future of Remote Work in 2026",
        content_type=ContentType.BLOG_POST,
        tone=Tone.PROFESSIONAL,
        length="medium",
        keywords=["remote work", "hybrid", "productivity", "work-life balance"],
        audience="business professionals and managers"
    ))
    print(blog)
    
    # Demo 2: Marketing Email
    print("\n\n--- MARKETING EMAIL ---\n")
    email = agent.write(ContentRequest(
        topic="Black Friday 50% off sale announcement",
        content_type=ContentType.EMAIL_MARKETING,
        tone=Tone.PERSUASIVE,
        audience="existing customers"
    ))
    print(email)
    
    # Demo 3: Twitter Posts
    print("\n\n--- TWITTER POSTS ---\n")
    tweets = agent.write(ContentRequest(
        topic="Launch of our new AI-powered productivity app",
        content_type=ContentType.SOCIAL_TWITTER,
        tone=Tone.FRIENDLY,
        audience="tech-savvy professionals"
    ))
    print(tweets)


if __name__ == "__main__":
    main()
