# Getting Started with MCP

A practical, hands-on guide to get you up and running with Model Context Protocol in under 30 minutes.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.10+** OR **Node.js 18+** (depending on your preference)
- **An MCP Client** for testing (choose one):
  - [Claude Desktop](https://claude.ai/download) - Easiest for beginners
  - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - CLI testing tool
  - [Continue.dev](https://continue.dev) - VS Code/JetBrains extension
- Basic command line knowledge
- A text editor (VS Code, Sublime, etc.)

## Step 1: Understand What MCP Is (5 minutes)

MCP (Model Context Protocol) is like a USB port for AI applications:

- **Without MCP**: Each AI app needs custom code to connect to every tool/data source
- **With MCP**: One standard protocol - any MCP server works with any MCP client

**Key Terms:**
- **MCP Server**: A program that exposes tools/data (you'll build this)
- **MCP Client**: An app that uses those tools (e.g., Claude Desktop, Continue.dev, MCP Inspector)
- **Tool**: A function the AI can call (e.g., "search_web", "read_file")
- **Resource**: Data the AI can read (e.g., files, database records)

## Step 2: Install Your Development Environment (5 minutes)

### Option A: Python

```bash
# Create a project directory
mkdir mcp-learning
cd mcp-learning

# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install MCP SDK
pip install mcp
```

### Option B: Node.js/TypeScript

```bash
# Create a project directory
mkdir mcp-learning
cd mcp-learning

# Initialize npm project
npm init -y

# Install MCP SDK
npm install @modelcontextprotocol/sdk

# Install TypeScript (if using TypeScript)
npm install -D typescript @types/node
```

## Step 3: Build Your First MCP Server (10 minutes)

### Python Version

Create `hello_server.py`:

```python
#!/usr/bin/env python3
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server
app = Server("hello-mcp")

# Define available tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="say_hello",
            description="Say hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person's name"}
                },
                "required": ["name"]
            }
        )
    ]

# Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "say_hello":
        person = arguments.get("name", "friend")
        return [TextContent(type="text", text=f"Hello, {person}! 👋")]
    raise ValueError(f"Unknown tool: {name}")

# Start server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

Make it executable:
```bash
chmod +x hello_server.py
```

### TypeScript Version

Create `hello_server.ts`:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "hello-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "say_hello",
      description: "Say hello to someone",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Person's name" },
        },
        required: ["name"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "say_hello") {
    const { name } = request.params.arguments as { name: string };
    return {
      content: [{ type: "text", text: `Hello, ${name}! 👋` }],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

Compile and run:
```bash
npx tsc hello_server.ts
node hello_server.js
```

## Step 4: Connect to an MCP Client (5 minutes)

Choose one of the following methods to test your server:

### Option A: MCP Inspector (Recommended for Learning)

The fastest way to test your server:

```bash
npx @modelcontextprotocol/inspector python /absolute/path/to/hello_server.py
```

This opens an interactive web interface where you can:
- See available tools
- Call tools with parameters
- View responses in real-time
- Debug protocol messages

### Option B: Claude Desktop

**Find your config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Edit the config:**

For Python:
```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/hello_server.py"]
    }
  }
}
```

For TypeScript/Node:
```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "node",
      "args": ["/absolute/path/to/hello_server.js"]
    }
  }
}
```

**Important:**
- Use ABSOLUTE paths, not relative
- Use forward slashes even on Windows: `C:/Users/...`
- If using Python venv, point to venv's Python: `/path/to/venv/bin/python`

**Restart Claude Desktop** completely for changes to take effect.

### Option C: Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "hello-mcp",
      "command": "python",
      "args": ["/absolute/path/to/hello_server.py"]
    }
  ]
}
```

Restart VS Code/JetBrains after configuration.

### Option D: Manual Testing (CLI)

Test the protocol directly:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python hello_server.py
```

## Step 5: Test It! (5 minutes)

### Using MCP Inspector

1. Open the inspector (from Step 4A)
2. Click on "say_hello" tool
3. Enter a name in the parameter field
4. Click "Call Tool"
5. See the response: "Hello, [name]! 👋"

### Using Claude Desktop

Open Claude Desktop and ask:

```
Can you use the say_hello tool to greet John?
```

You should see Claude use your tool and return "Hello, John! 👋"

### Using Continue.dev

In your IDE, open Continue and ask:

```
Use the say_hello tool to greet Alice
```

### Troubleshooting

**Server not detected:**
1. Verify absolute paths in config
2. Test server manually: `python hello_server.py` (should wait for input)
3. Check logs:
   - Claude Desktop: `~/Library/Logs/Claude/` (macOS) or `%APPDATA%\Claude\logs\` (Windows)
   - MCP Inspector: shows errors in the UI
   - Continue.dev: Check VS Code output panel
4. Ensure server file is executable (Unix): `chmod +x hello_server.py`
5. Verify dependencies installed: `pip list | grep mcp` or `npm list`

## Next Steps

### Add More Tools

Extend your server with additional tools:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="say_hello", ...),
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        )
    ]
```

### Add Resources

Let the AI read data:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///notes.txt",
            name="My Notes",
            mimeType="text/plain"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "file:///notes.txt":
        return "These are my notes..."
    raise ValueError(f"Unknown resource: {uri}")
```

### Explore Examples

Check out the `examples/` directory in this repository for:
- Weather API integration
- File system operations
- Calculator with multiple tools
- Database queries

### Learn More

- Read the full [README.md](README.md) for comprehensive resources
- Join the [MCP Discord community](https://discord.gg/anthropic)
- Browse [official examples](https://github.com/modelcontextprotocol/servers)

## Common Issues & Solutions

### "Server not found" in Claude Desktop

- Double-check the absolute path in config
- Ensure file has execute permissions (Unix): `chmod +x server.py`
- Verify Python/Node is in your PATH

### "Tool not available"

- Restart Claude Desktop after config changes
- Check server logs for errors
- Verify tool schema is valid JSON

### Server crashes immediately

- Check Python/Node version compatibility
- Look for syntax errors in your code
- Test server manually from command line

### Claude doesn't use the tool

- Make tool description clear and specific
- Use descriptive parameter names
- Test with direct prompts: "Use the X tool to..."

## Pro Tips

1. **Start Simple**: Begin with one tool, add more once it works
2. **Use Logging**: Log to stderr (stdout is for MCP protocol)
3. **Test Independently**: Run your server manually to debug
4. **Read Examples**: Study the official example servers
5. **Join Community**: Ask questions in Discord/GitHub discussions

## Congratulations!

You've built and deployed your first MCP server! You now understand:
- What MCP is and why it matters
- How to create MCP servers
- How to connect them to Claude Desktop
- How to test and debug

Ready to build something more complex? Check out the full [README.md](README.md) for advanced tutorials and examples.
