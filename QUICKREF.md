# MCP Quick Reference

A cheat sheet for Model Context Protocol development.

## Architecture Overview

```
┌─────────────────┐
│   MCP Client    │  (Claude Desktop, IDEs, Custom Apps)
│                 │
│  - Discovers    │
│  - Calls Tools  │
│  - Reads Data   │
└────────┬────────┘
         │ MCP Protocol (JSON-RPC over stdio/HTTP)
         │
┌────────▼────────┐
│   MCP Server    │  (Your Custom Server)
│                 │
│  • Tools        │  Functions AI can call
│  • Resources    │  Data AI can read
│  • Prompts      │  Reusable templates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Your Services  │  (APIs, Databases, Files, etc.)
└─────────────────┘
```

## Core Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Server** | Program exposing functionality via MCP | Weather server, DB connector |
| **Client** | Application using MCP servers | Claude Desktop, Continue.dev |
| **Tool** | Function that AI can invoke | `search_files`, `send_email` |
| **Resource** | Data source AI can read | File contents, DB records |
| **Prompt** | Reusable prompt template | Code review template |
| **Transport** | Communication method | stdio, HTTP, WebSocket |

## MCP Protocol Flow

### 1. Initialization
```
Client → Server: initialize request
Server → Client: initialize response (capabilities)
Client → Server: initialized notification
```

### 2. Discovery
```
Client → Server: tools/list, resources/list, prompts/list
Server → Client: Available tools, resources, prompts
```

### 3. Usage
```
Client → Server: tools/call, resources/read, prompts/get
Server → Client: Results
```

## Creating a Server

### Minimum Viable Server (Python)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("my-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="my_tool", description="...", inputSchema={...})]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    return [TextContent(type="text", text="result")]

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())
```

### Minimum Viable Server (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{ name: "my_tool", description: "...", inputSchema: {...} }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => ({
  content: [{ type: "text", text: "result" }]
}));

await server.connect(new StdioServerTransport());
```

## Tool Schema Reference

### Basic Tool Definition

```json
{
  "name": "tool_name",
  "description": "Clear description of what this tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "What this parameter is for"
      },
      "param2": {
        "type": "number",
        "description": "Numeric parameter",
        "minimum": 0
      }
    },
    "required": ["param1"]
  }
}
```

### Common Schema Types

```json
{
  "string": { "type": "string" },
  "number": { "type": "number" },
  "boolean": { "type": "boolean" },
  "array": {
    "type": "array",
    "items": { "type": "string" }
  },
  "object": {
    "type": "object",
    "properties": { ... }
  },
  "enum": {
    "type": "string",
    "enum": ["option1", "option2"]
  }
}
```

## Resource Schema Reference

### Basic Resource Definition

```python
Resource(
    uri="scheme://path/to/resource",
    name="Human Readable Name",
    description="What this resource contains",
    mimeType="text/plain"  # or "application/json", etc.
)
```

### Common URI Schemes

- `file:///path/to/file` - Local files
- `http://` or `https://` - Web resources
- `db:///table/id` - Database records
- Custom schemes for your domain

## Claude Desktop Configuration

### Config File Locations

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Basic Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

### With Environment Variables

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here",
        "DEBUG": "true"
      }
    }
  }
}
```

### Multiple Servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    },
    "custom": {
      "command": "python",
      "args": ["/path/to/custom_server.py"]
    }
  }
}
```

## Common Patterns

### Error Handling (Python)

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = perform_operation(arguments)
        return [TextContent(type="text", text=str(result))]
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {e}")]
```

### Async API Calls (Python)

```python
import httpx

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{arguments['query']}")
        data = response.json()
        return [TextContent(type="text", text=str(data))]
```

### File Operations (Python)

```python
from pathlib import Path

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("file:///"):
        path = Path(uri[7:])  # Remove file:/// prefix
        if path.exists() and path.is_file():
            return path.read_text()
    raise ValueError(f"Resource not found: {uri}")
```

## Testing Your Server

### Manual Testing (stdio)

```bash
# Start your server
python server.py

# Send a request (type this as JSON)
{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}

# Press Ctrl+D to send
```

### Using MCP Inspector

```bash
# Install
npm install -g @modelcontextprotocol/inspector

# Run
mcp-inspector python /path/to/server.py
```

### Unit Testing (Python)

```python
import pytest
from your_server import app

@pytest.mark.asyncio
async def test_tool():
    tools = await app.list_tools()
    assert len(tools) > 0

    result = await app.call_tool("tool_name", {"param": "value"})
    assert result[0].text == "expected output"
```

## Debugging Tips

### Enable Logging (Python)

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    # Log to file, not stdout (stdout is for MCP protocol)
    filename='server.log'
)

logger = logging.getLogger(__name__)
```

### Check Claude Desktop Logs

```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Windows
type %APPDATA%\Claude\logs\mcp*.log

# Linux
tail -f ~/.config/Claude/logs/mcp*.log
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Server not appearing | Check absolute paths, restart Claude Desktop |
| Tool not being called | Improve tool description, make it more specific |
| Connection errors | Verify stdio transport, check for syntax errors |
| Import errors | Check dependencies installed, virtual env activated |

## Best Practices

### Security
- ✅ Validate all inputs from LLM
- ✅ Use environment variables for secrets
- ✅ Implement proper permissions
- ❌ Never hardcode API keys
- ❌ Don't trust tool arguments blindly

### Performance
- ✅ Cache frequently accessed data
- ✅ Use async/await for I/O operations
- ✅ Implement timeouts
- ❌ Don't block on long operations
- ❌ Avoid loading large data synchronously

### User Experience
- ✅ Clear, descriptive tool names
- ✅ Detailed parameter descriptions
- ✅ Meaningful error messages
- ❌ Don't use technical jargon in descriptions
- ❌ Avoid overly generic tool names

## Useful Commands

```bash
# Install Python MCP SDK
pip install mcp

# Install TypeScript MCP SDK
npm install @modelcontextprotocol/sdk

# Run MCP Inspector
npx @modelcontextprotocol/inspector python server.py

# Test server manually
python server.py < test_input.json

# Check server is running
ps aux | grep server.py

# View Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/mcp*.log
```

## Resources

- [Official Docs](https://modelcontextprotocol.io)
- [Specification](https://spec.modelcontextprotocol.io)
- [GitHub Org](https://github.com/modelcontextprotocol)
- [Example Servers](https://github.com/modelcontextprotocol/servers)
- [Discord Community](https://discord.gg/anthropic)

## JSON-RPC Messages

### Request Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param": "value"
    }
  }
}
```

### Response Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "result data"
      }
    ]
  }
}
```

### Error Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

---

Keep this reference handy while developing MCP servers!
