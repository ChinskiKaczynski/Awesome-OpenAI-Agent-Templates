# Code Review Agent

An AI agent that reviews code and provides constructive feedback.

## Features

- 🔍 **Code Analysis**: Identify issues and improvements
- 🐛 **Bug Detection**: Spot potential bugs and edge cases
- 🎨 **Style Review**: Check code style and conventions
- 📈 **Performance Tips**: Suggest optimizations
- 📚 **Best Practices**: Recommend patterns and practices
- ✅ **Security Scan**: Identify security vulnerabilities

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Review Types

| Type | Focus |
|------|-------|
| `full` | Complete review |
| `security` | Security vulnerabilities |
| `performance` | Performance optimizations |
| `style` | Code style and conventions |
| `bugs` | Bug detection |

## Example

```python
from main import CodeReviewAgent, ReviewRequest, ReviewType

agent = CodeReviewAgent()
review = agent.review(ReviewRequest(
    code="def add(a, b): return a + b",
    language="python",
    review_type=ReviewType.FULL,
))
print(review)
```

## Output Format

```markdown
## Code Review Summary

### Overall Score: 7/10

### Issues Found
- 🔴 Critical: SQL injection risk on line 42
- 🟡 Warning: Unused variable 'temp' on line 15
- 🟢 Suggestion: Consider using list comprehension

### Recommendations
1. Use parameterized queries
2. Add input validation
3. Consider caching for repeated calls

### Improved Code
```python
# Fixed version with comments
```
