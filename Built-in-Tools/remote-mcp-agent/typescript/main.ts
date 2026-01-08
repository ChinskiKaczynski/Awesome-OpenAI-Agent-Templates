/**
 * Remote MCP Agent
 * Connect to external tools and services using the Model Context Protocol.
 */
import OpenAI from "openai";

const openai = new OpenAI();

interface MCPServer {
    type: "mcp";
    server_label: string;
    server_url: string;
    require_approval: "never" | "always";
}

class RemoteMCPAgent {
    private model: string;
    private mcpServers: MCPServer[];

    constructor(model: string = "gpt-4o-mini") {
        this.model = model;
        this.mcpServers = [];
    }

    addMCPServer(
        label: string,
        url: string,
        requireApproval: "never" | "always" = "never"
    ): void {
        this.mcpServers.push({
            type: "mcp",
            server_label: label,
            server_url: url,
            require_approval: requireApproval,
        });
        console.log(`🔌 Added MCP server: ${label} -> ${url}`);
    }

    async execute(prompt: string): Promise<string> {
        if (this.mcpServers.length === 0) {
            return "No MCP servers registered. Use addMCPServer() first.";
        }

        console.log(`🤖 Executing: ${prompt}`);
        console.log(`   MCP servers: ${this.mcpServers.length}`);

        const response = await openai.responses.create({
            model: this.model,
            input: prompt,
            tools: this.mcpServers,
        });

        // Log tool calls
        for (const output of response.output) {
            if (output.type === "mcp_call") {
                console.log(`   🔧 MCP call: ${output.server_label}`);
            }
        }

        return response.output_text;
    }
}

async function main() {
    console.log("=".repeat(50));
    console.log("🔌 REMOTE MCP AGENT DEMO");
    console.log("=".repeat(50));

    const agent = new RemoteMCPAgent();

    console.log("\n📝 Note: This demo shows the API structure.");
    console.log("   Replace the example URL with your MCP server.\n");

    const exampleConfig = `
    // To use a real MCP server:
    
    agent.addMCPServer(
        "github",
        "https://mcp.github.com/v1",  // hypothetical
        "never"
    );
    
    agent.addMCPServer(
        "slack",
        "https://mcp.slack.com/v1",  // hypothetical
        "always"  // require approval for message sends
    );
    
    // Then execute:
    const result = await agent.execute("List my recent GitHub notifications");
    `;

    console.log(exampleConfig);

    console.log("\n--- Example API Structure ---\n");
    console.log(`
    openai.responses.create({
        model: "gpt-4o-mini",
        input: "List my GitHub issues",
        tools: [
            {
                type: "mcp",
                server_label: "github",
                server_url: "https://mcp.example.com",
                require_approval: "never",
            }
        ]
    });
    `);

    console.log("\n" + "=".repeat(50));
    console.log("See: https://modelcontextprotocol.io/ for MCP documentation");
}

main();
