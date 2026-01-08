# Content Writer Agent

An AI agent that writes high-quality content including blog posts, emails, and marketing copy.

## Features

- ✍️ **Blog Posts**: SEO-optimized articles
- 📧 **Emails**: Professional and marketing emails
- 📱 **Social Media**: Posts for various platforms
- 📢 **Marketing Copy**: Ads, landing pages, CTAs
- 🔄 **Rewriting**: Improve existing content

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Content Types

| Type | Description |
|------|-------------|
| `blog_post` | Long-form article with headings |
| `email_marketing` | Promotional email |
| `email_professional` | Business correspondence |
| `social_twitter` | Short-form social post |
| `social_linkedin` | Professional social post |
| `ad_copy` | Short advertisement |
| `landing_page` | Web page copy |

## Example Prompts

```
"Write a blog post about the benefits of remote work"
"Create a launch email for our new product"
"Write 5 tweet variations for our sale announcement"
```

## Customization

```python
result = agent.write(
    content_type="blog_post",
    topic="AI in Healthcare",
    tone="professional",
    length="long",
    keywords=["AI", "healthcare", "diagnosis"],
    audience="healthcare professionals"
)
```
