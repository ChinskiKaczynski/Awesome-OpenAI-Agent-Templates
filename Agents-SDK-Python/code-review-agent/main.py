"""
Code Review Agent
An AI agent that reviews code and provides constructive feedback.

Analyzes code for bugs, style, performance, and security issues.
"""
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
from dataclasses import dataclass

load_dotenv()

client = OpenAI()


class ReviewType(Enum):
    FULL = "full"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    BUGS = "bugs"


@dataclass
class ReviewRequest:
    """Code review request."""
    code: str
    language: str = "python"
    review_type: ReviewType = ReviewType.FULL
    context: str = ""  # Additional context about the code


REVIEW_PROMPTS = {
    ReviewType.FULL: """Perform a comprehensive code review covering:
1. **Bugs & Logic Errors**: Identify potential bugs, edge cases, null/undefined issues
2. **Security**: Check for vulnerabilities (injection, XSS, auth issues)
3. **Performance**: Identify inefficiencies and optimization opportunities
4. **Code Style**: Check naming conventions, formatting, readability
5. **Best Practices**: Suggest patterns and improvements
6. **Documentation**: Evaluate comments and documentation""",

    ReviewType.SECURITY: """Focus specifically on security vulnerabilities:
1. **Injection Attacks**: SQL, command, LDAP, XPath injection
2. **Authentication/Authorization**: Weak auth, missing checks
3. **Data Exposure**: Sensitive data logging, insecure storage
4. **Input Validation**: Missing or weak validation
5. **Cryptography**: Weak algorithms, hardcoded secrets
6. **Dependencies**: Known vulnerable libraries""",

    ReviewType.PERFORMANCE: """Focus specifically on performance:
1. **Time Complexity**: O(n²) or worse algorithms
2. **Memory Usage**: Memory leaks, excessive allocation
3. **Database Queries**: N+1 problems, missing indexes
4. **Caching**: Opportunities for caching
5. **Concurrency**: Race conditions, deadlocks
6. **I/O Operations**: Blocking operations, inefficient I/O""",

    ReviewType.STYLE: """Focus specifically on code style:
1. **Naming**: Clear, consistent naming conventions
2. **Formatting**: Proper indentation, line length
3. **Structure**: Function/class organization
4. **Readability**: Complex expressions, magic numbers
5. **Comments**: Appropriate, helpful comments
6. **Consistency**: Consistent patterns throughout""",

    ReviewType.BUGS: """Focus specifically on bug detection:
1. **Logic Errors**: Incorrect conditions, off-by-one
2. **Null/Undefined**: Null pointer issues
3. **Type Errors**: Type mismatches
4. **Edge Cases**: Empty arrays, boundary values
5. **Error Handling**: Missing try/catch, swallowed exceptions
6. **Race Conditions**: Concurrency bugs""",
}


class CodeReviewAgent:
    """Agent that reviews code and provides feedback."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    
    def review(self, request: ReviewRequest) -> str:
        """Review code and generate feedback."""
        print(f"🔍 Reviewing {request.language} code...")
        print(f"   Review type: {request.review_type.value}")
        
        focus_prompt = REVIEW_PROMPTS[request.review_type]
        
        prompt = f"""You are an expert code reviewer. Review this {request.language} code.

{focus_prompt}

{f"Context: {request.context}" if request.context else ""}

CODE TO REVIEW:
```{request.language}
{request.code}
```

Provide your review in this format:

## Code Review Summary

### Overall Score: X/10

### Issues Found
List each issue with severity:
- 🔴 Critical: [description] (line X)
- 🟡 Warning: [description] (line X)  
- 🟢 Suggestion: [description]

### Recommendations
Numbered list of specific improvements

### Improved Code (if applicable)
Show fixed version of problematic sections with comments explaining changes.

Be specific, constructive, and educational. Explain WHY each issue matters."""

        response = client.responses.create(
            model=self.model,
            input=prompt,
        )
        
        return response.output_text
    
    def explain(self, code: str, language: str = "python") -> str:
        """Explain what code does."""
        print("📖 Generating code explanation...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Explain this {language} code clearly:

```{language}
{code}
```

Provide:
1. High-level summary (what it does)
2. Step-by-step walkthrough
3. Key concepts used
4. Potential use cases"""
        )
        
        return response.output_text
    
    def suggest_tests(self, code: str, language: str = "python") -> str:
        """Suggest test cases for code."""
        print("🧪 Generating test suggestions...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Suggest test cases for this {language} code:

```{language}
{code}
```

Provide:
1. Unit tests for each function/method
2. Edge cases to test
3. Example test code using appropriate testing framework
4. Integration test ideas if applicable"""
        )
        
        return response.output_text


# Sample code for demo
SAMPLE_CODE = '''
def get_user_data(user_id):
    """Get user data from database."""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result[0]

def calculate_discount(price, discount):
    return price - (price * discount / 100)

def process_items(items):
    processed = []
    for i in range(len(items)):
        item = items[i]
        if item['status'] == 'active':
            item['processed'] = True
            processed.append(item)
    return processed

def send_notification(user, message):
    try:
        api.send(user.email, message)
    except:
        pass
    return True
'''


def main():
    """Demo the code review agent."""
    agent = CodeReviewAgent()
    
    print("="*50)
    print("🔍 CODE REVIEW AGENT DEMO")
    print("="*50)
    print("\nSample Code:")
    print(SAMPLE_CODE)
    print("="*50)
    
    # Full review
    print("\n\n--- FULL CODE REVIEW ---\n")
    review = agent.review(ReviewRequest(
        code=SAMPLE_CODE,
        language="python",
        review_type=ReviewType.FULL,
        context="This is part of a web application backend"
    ))
    print(review)
    
    # Security-focused review
    print("\n\n--- SECURITY REVIEW ---\n")
    security_review = agent.review(ReviewRequest(
        code=SAMPLE_CODE,
        language="python",
        review_type=ReviewType.SECURITY
    ))
    print(security_review)
    
    # Test suggestions
    print("\n\n--- TEST SUGGESTIONS ---\n")
    tests = agent.suggest_tests(SAMPLE_CODE, "python")
    print(tests)


if __name__ == "__main__":
    main()
