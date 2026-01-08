"""
Remote MCP Agent
Connect to external tools and services using the Model Context Protocol.

MCP allows you to expose external tools to the model securely.
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


class RemoteMCPAgent:
    """Agent that connects to remote MCP servers for external tools."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.mcp_servers = []
    
    def add_mcp_server(
        self, 
        label: str, 
        url: str, 
        require_approval: str = "never"
    ):
        """
        Register an MCP server.
        
        Args:
            label: Unique identifier for this server
            url: HTTPS URL of the MCP server
            require_approval: "never" or "always"
        """
        self.mcp_servers.append({
            "type": "mcp",
            "server_label": label,
            "server_url": url,
            "require_approval": require_approval,
        })
        print(f"🔌 Added MCP server: {label} -> {url}")
    
    def execute(self, prompt: str) -> str:
        """
        Execute a prompt with access to all registered MCP servers.
        
        Args:
            prompt: The user's request
        
        Returns:
            Agent's response
        """
        if not self.mcp_servers:
            return "No MCP servers registered. Use add_mcp_server() first."
        
        print(f"🤖 Executing: {prompt}")
        print(f"   MCP servers: {len(self.mcp_servers)}")
        
        response = client.responses.create(
            model=self.model,
            input=prompt,
            tools=self.mcp_servers,
        )
        
        # Log tool calls
        for output in response.output:
            if hasattr(output, 'type') and output.type == "mcp_call":
                print(f"   🔧 MCP call: {output.server_label}")
        
        return response.output_text


def main():
    """Demo the remote MCP agent."""
    print("="*50)
    print("🔌 REMOTE MCP AGENT DEMO")
    print("="*50)
    
    agent = RemoteMCPAgent()
    
    # Example: Add a hypothetical MCP server
    # In production, replace with your actual MCP server URL
    print("\n📝 Note: This demo shows the API structure.")
    print("   Replace the example URL with your MCP server.\n")
    
    # Simulated MCP server configuration
    example_config = """
    # To use a real MCP server:
    
    agent.add_mcp_server(
        label="github",
        url="https://mcp.github.com/v1",  # hypothetical
        require_approval="never"
    )
    
    agent.add_mcp_server(
        label="slack",
        url="https://mcp.slack.com/v1",  # hypothetical
        require_approval="always"  # require approval for message sends
    )
    
    # Then execute:
    result = agent.execute("List my recent GitHub notifications")
    """
    
    print(example_config)
    
    # Demo with mock response
    print("\n--- Example API Structure ---\n")
    print("Request:")
    print("""
    client.responses.create(
        model="gpt-4o-mini",
        input="List my GitHub issues",
        tools=[
            {
                "type": "mcp",
                "server_label": "github",
                "server_url": "https://mcp.example.com",
                "require_approval": "never",
            }
        ]
    )
    """)
    
    print("\n" + "="*50)
    print("See: https://modelcontextprotocol.io/ for MCP documentation")


if __name__ == "__main__":
    main()
