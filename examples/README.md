# MCP Examples

Practical code examples to help you get started with Model Context Protocol.

## Directory Structure

- `python/` - Python MCP server examples
- `typescript/` - TypeScript/JavaScript MCP server examples

## Quick Start Examples

### Python

1. **Simple Tool Server** (`python/simple_tool.py`)
   - Basic MCP server with a single tool
   - Perfect first example
   - Run: `python simple_tool.py`

2. **Weather Server** (`python/weather_server.py`)
   - Integrates with external API
   - Shows async/await patterns
   - Demonstrates error handling

3. **File Notes Server** (`python/notes_server.py`)
   - Resource-based server
   - File system operations
   - CRUD operations

### TypeScript

1. **Simple Tool Server** (`typescript/simple-tool.ts`)
   - Basic MCP server with a single tool
   - TypeScript types and interfaces
   - Run: `npm install && npm start`

2. **Calculator Server** (`typescript/calculator.ts`)
   - Multiple tools example
   - Input validation
   - Complex schemas

3. **Database Server** (`typescript/database.ts`)
   - SQLite integration
   - Safe query execution
   - Schema introspection

## Usage

Each example includes:
- Fully commented code
- Setup instructions
- Configuration for Claude Desktop
- Testing tips

## Testing Your Server

1. **With Claude Desktop**:
   - Add server to `claude_desktop_config.json`
   - Restart Claude Desktop
   - Test by asking Claude to use the tools

2. **With MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector python examples/python/simple_tool.py
   ```

3. **Direct Testing**:
   - Run the server
   - Send JSON-RPC messages via stdin
   - Verify responses on stdout

## Contributing Examples

Have a great example? Submit a PR!

Requirements:
- Well-commented code
- README with setup instructions
- Tested and working
- Demonstrates a clear concept
