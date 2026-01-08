# Remote MCP Agent

Connect to external tools and services using the **Model Context Protocol (MCP)**.

> 📚 **MCP Docs**: <https://modelcontextprotocol.io/>

## Usage

```bash
pip install -r requirements.txt
python main.py
```

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
| `require_approval: never` | Auto-execute tools |
| `require_approval: always` | User confirms each call |

## Supported Transports

- **HTTPS** - Remote servers over TLS
- **stdio** - Local process communication

## Use Cases

- Access external APIs securely
- Integrate with enterprise systems
- Connect to custom tool servers
- Enable multi-service workflows
