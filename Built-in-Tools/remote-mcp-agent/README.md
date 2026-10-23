# Remote MCP Agent

Connect to external tools and services using the **Model Context Protocol (MCP)**.

> 📚 **MCP Docs**: <https://modelcontextprotocol.io/>

## Usage

```bash
cd python
pip install -r requirements.txt
python main.py
```

> **Demo only:** The Python and TypeScript entry points print example configurations; neither makes a live MCP request. To use a server, supply a real endpoint and call the agent's `execute()` method from your application.

## What it does

1. Connects to remote MCP servers
2. Exposes external tools to the model
3. Enables agents to use third-party services

## Example MCP Servers

| Server | Description |
|--------|-------------|
| Filesystem | Read/write local files |
| Database | Query SQL databases |
| GitHub | Interact with repositories |
| Slack | Send messages |
| Custom | Your own tools |

## How It Works

```
Agent Request
      ↓
┌───────────────┐
│   Remote MCP  │ ← Connect to external server
│   Tool        │
└───────┬───────┘
        ↓
   External API
        ↓
   Tool Result
```

## Configuration

```python
tools = [
    {
        "type": "mcp",
        "server_label": "my-server",
        "server_url": "https://mcp.example.com",
        "require_approval": "never",  # or "always"
    }
]
```

## Security

| Setting | Description |
|---------|-------------|
| `require_approval: never` | Skip approvals for all MCP tools on this server; only use with trusted servers and suitable permissions. |
| `require_approval: always` | The API returns an `mcp_approval_request` for each tool call. Your application must review it and send an `mcp_approval_response` in a follow-up Responses request. |

**Limitation:** These demo scripts do not implement the approval continuation. Setting `always` does not automatically ask the user for approval or finish the tool call.

## Supported Transports

- **Streamable HTTP** - Remote MCP server via `server_url`.
- **HTTP/SSE** - Remote MCP server via `server_url`.

Local **stdio** servers are not supported by this Responses API `server_url` example. The Agents SDK and Agents API provide separate local MCP integrations.

See the [OpenAI Responses MCP guide](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) for supported transports and the approval flow.

## Use Cases

- Access external APIs securely
- Integrate with enterprise systems
- Connect to custom tool servers
- Enable multi-service workflows
