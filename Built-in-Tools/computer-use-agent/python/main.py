"""
Computer Use Agent
Browser and desktop automation using the computer_use_preview built-in tool.

⚠️ Preview Feature: This API is in preview and may change.
"""
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class ComputerUseAgent:
    """Agent that automates browser/desktop tasks."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    
    def execute_task(self, task: str, environment: str = "browser") -> dict:
        """
        Execute a computer use task.
        
        Args:
            task: Natural language description of what to do
            environment: 'browser' or 'computer'
        
        Returns:
            Dict with result and any extracted data
        """
        print(f"🖥️  Task: {task}")
        print(f"   Environment: {environment}")
        print("   Running...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""You are a computer use assistant. Complete this task:

Task: {task}

Use the computer_use tool to:
1. Navigate to the appropriate website/application
2. Perform the necessary actions (click, type, scroll)
3. Extract and return the requested information

Be methodical and verify each step.""",
            tools=[
                {
                    "type": "computer_use_preview",
                    "display_width": 1024,
                    "display_height": 768,
                    "environment": environment,
                }
            ]
        )
        
        # Parse the response
        result = {
            "task": task,
            "output": response.output_text,
            "steps": []
        }
        
        # Extract computer use steps
        for output in response.output:
            if hasattr(output, 'type') and output.type == "computer_call":
                step = {
                    "action": output.action.type if hasattr(output.action, 'type') else str(output.action),
                }
                result["steps"].append(step)
                print(f"   📸 Action: {step['action']}")
        
        return result
    
    def scrape_page(self, url: str, extract: str) -> str:
        """
        Navigate to a URL and extract specific information.
        
        Args:
            url: Website to visit
            extract: What information to extract
        
        Returns:
            Extracted information
        """
        task = f"Go to {url} and extract: {extract}"
        result = self.execute_task(task)
        return result["output"]
    
    def fill_form(self, url: str, form_data: dict) -> bool:
        """
        Navigate to a URL and fill out a form.
        
        Args:
            url: Page with the form
            form_data: Dict of field names to values
        
        Returns:
            Success status
        """
        fields_str = ", ".join([f"{k}: {v}" for k, v in form_data.items()])
        task = f"Go to {url} and fill the form with: {fields_str}. Do not submit."
        result = self.execute_task(task)
        return "error" not in result["output"].lower()


def main():
    """Demo the computer use agent."""
    agent = ComputerUseAgent()
    
    print("="*50)
    print("🖥️  COMPUTER USE AGENT DEMO")
    print("="*50)
    print("\n⚠️  Note: This is a preview feature")
    print("   Requires computer_use_preview access\n")
    
    # Demo 1: Simple scraping task
    print("\n--- Task 1: Information Extraction ---\n")
    result = agent.execute_task(
        "Go to example.com and tell me what the main heading says"
    )
    print(f"✅ Result: {result['output']}")
    
    # Demo 2: Search task
    print("\n--- Task 2: Search ---\n")
    result = agent.execute_task(
        "Use a search engine to find the current weather in New York"
    )
    print(f"✅ Result: {result['output']}")
    
    print("\n" + "="*50)
    print("Demo complete!")
    print("For production use, ensure proper sandboxing and monitoring.")


if __name__ == "__main__":
    main()
