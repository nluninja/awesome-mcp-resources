# Awesome MCP Resources

A curated list of resources for learning and working with Model Context Protocol (MCP) - a practical guide for students and developers to get started quickly.

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Quick Start](#quick-start)
- [Official Documentation](#official-documentation)
- [Courses & Tutorials](#courses--tutorials)
- [Video Resources](#video-resources)
- [Example Projects](#example-projects)
- [MCP Servers](#mcp-servers)
- [Client Implementations](#client-implementations)
- [Tools & Libraries](#tools--libraries)
- [Community Resources](#community-resources)
- [Best Practices](#best-practices)

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables seamless integration between AI models and data sources, tools, and services.

### Key Concepts

- **MCP Servers**: Programs that expose data and functionality through the MCP protocol
- **MCP Clients**: Applications (like Claude Desktop, IDEs) that connect to MCP servers
- **Resources**: Data sources that servers make available to clients
- **Tools**: Functions that LLMs can invoke through the protocol
- **Prompts**: Reusable prompt templates exposed by servers

### Why MCP Matters

- Standardized way to connect AI to external data and tools
- Eliminates custom integrations for each AI application
- Enables modular, composable AI systems
- Open protocol supported by Anthropic and growing community

## Quick Start

### Prerequisites

- Node.js 18+ or Python 3.10+
- Basic understanding of REST APIs and JSON
- An MCP-compatible client (Claude Desktop recommended for beginners)

### 5-Minute Setup

1. **Install Claude Desktop** (easiest way to test MCP servers)
   - Download from [claude.ai/download](https://claude.ai/download)

2. **Create your first MCP server** (choose one):

   **Python Example:**
   ```bash
   pip install mcp
   ```

   ```python
   # server.py
   from mcp.server import Server
   from mcp.server.stdio import stdio_server

   app = Server("my-first-server")

   @app.list_tools()
   async def list_tools():
       return [{"name": "greet", "description": "Greet someone", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}}}]

   @app.call_tool()
   async def call_tool(name: str, arguments: dict):
       if name == "greet":
           return [{"type": "text", "text": f"Hello, {arguments['name']}!"}]

   async def main():
       async with stdio_server() as streams:
           await app.run(streams[0], streams[1], app.create_initialization_options())

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())
   ```

   **TypeScript Example:**
   ```bash
   npm install @modelcontextprotocol/sdk
   ```

   ```typescript
   // server.ts
   import { Server } from "@modelcontextprotocol/sdk/server/index.js";
   import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

   const server = new Server({
     name: "my-first-server",
     version: "1.0.0"
   }, {
     capabilities: { tools: {} }
   });

   server.setRequestHandler("tools/list", async () => ({
     tools: [{
       name: "greet",
       description: "Greet someone",
       inputSchema: {
         type: "object",
         properties: { name: { type: "string" } }
       }
     }]
   }));

   server.setRequestHandler("tools/call", async (request) => {
     if (request.params.name === "greet") {
       return {
         content: [{ type: "text", text: `Hello, ${request.params.arguments.name}!` }]
       };
     }
   });

   const transport = new StdioServerTransport();
   await server.connect(transport);
   ```

3. **Configure Claude Desktop** to use your server:

   Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

   ```json
   {
     "mcpServers": {
       "my-first-server": {
         "command": "python",
         "args": ["/path/to/server.py"]
       }
     }
   }
   ```

4. **Restart Claude Desktop** and test your server!

## Official Documentation

- [MCP Documentation](https://modelcontextprotocol.io) - Official documentation and specification
- [MCP Specification](https://spec.modelcontextprotocol.io) - Technical protocol specification
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol) - Original announcement blog post
- [GitHub Repository](https://github.com/modelcontextprotocol) - Official MCP organization

## Courses & Tutorials

### Beginner-Friendly

- **[MCP Quickstart Guide](https://modelcontextprotocol.io/quickstart)** (30 minutes)
  - Official quickstart tutorial
  - Covers basic concepts and first server
  - No prior MCP knowledge needed

- **[Building Your First MCP Server](https://modelcontextprotocol.io/tutorials/building-mcp-server)** (1 hour)
  - Step-by-step tutorial
  - Python and TypeScript examples
  - Includes testing and debugging

- **[MCP for Beginners](https://www.youtube.com/results?search_query=model+context+protocol+tutorial)** (Video series)
  - Visual walkthrough of core concepts
  - Practical examples
  - Common pitfalls and solutions

### Intermediate

- **[Building Production MCP Servers](https://modelcontextprotocol.io/tutorials/production-servers)** (2-3 hours)
  - Error handling and logging
  - Security best practices
  - Performance optimization

- **[Integrating MCP with Existing APIs](https://modelcontextprotocol.io/tutorials/api-integration)** (2 hours)
  - Connect MCP to REST APIs
  - Database integration patterns
  - Authentication and authorization

### Advanced

- **[Custom Transport Layers](https://modelcontextprotocol.io/tutorials/custom-transports)** (3 hours)
  - Beyond stdio: HTTP, WebSocket transports
  - Building custom transport mechanisms
  - Network-based MCP servers

- **[MCP Server Optimization](https://modelcontextprotocol.io/tutorials/optimization)** (2 hours)
  - Caching strategies
  - Concurrent request handling
  - Resource management

## Video Resources

### Introductory Videos

- [What is Model Context Protocol?](https://www.youtube.com/results?search_query=what+is+model+context+protocol) - 10-minute overview
- [MCP Demo and Walkthrough](https://www.youtube.com/results?search_query=mcp+demo) - Live demonstration
- [Building Your First MCP Server](https://www.youtube.com/results?search_query=building+mcp+server) - 30-minute tutorial

### Conference Talks

- Anthropic's MCP Launch Presentation
- MCP at AI Engineer Summit
- Building AI Agents with MCP

### Community Tutorials

- Setting up MCP with Claude Desktop
- MCP Server Development Tips
- Real-world MCP Use Cases

## Example Projects

### Official Examples

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers) - Official collection of reference servers
  - File system server
  - Database connectors (PostgreSQL, SQLite)
  - GitHub integration
  - Google Drive integration
  - Slack integration

### Community Examples

#### Beginner Level

- **Weather Server** - Simple API integration example
  - Fetches weather data from external API
  - Demonstrates tool implementation
  - [Example Code](https://github.com/modelcontextprotocol/servers/tree/main/src/weather)

- **Calculator Server** - Basic tool demonstration
  - Simple arithmetic operations
  - Shows tool parameter handling
  - Great first project

- **Note-taking Server** - File-based resource example
  - Read/write notes
  - List available notes
  - Demonstrates resource management

#### Intermediate Level

- **Database Query Server** - SQL database integration
  - Connect to PostgreSQL/MySQL
  - Safe query execution
  - Schema introspection

- **Git Repository Server** - Version control integration
  - Repository browsing
  - Commit history access
  - File content retrieval

- **Web Scraper Server** - Dynamic content fetching
  - URL content extraction
  - HTML parsing
  - Rate limiting implementation

#### Advanced Level

- **Multi-API Aggregator** - Combines multiple services
  - Coordinates multiple API calls
  - Data transformation and merging
  - Complex tool orchestration

- **RAG Document Server** - Vector search integration
  - Document embedding
  - Semantic search
  - Context retrieval for LLMs

- **Development Environment Server** - IDE integration
  - Code execution
  - Linting and formatting
  - Test running

## MCP Servers

### Official Servers

| Server | Description | Language | Use Case |
|--------|-------------|----------|----------|
| [filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | File system operations | TypeScript | Read/write local files |
| [github](https://github.com/modelcontextprotocol/servers/tree/main/src/github) | GitHub API integration | TypeScript | Repository management |
| [gitlab](https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab) | GitLab API integration | TypeScript | GitLab operations |
| [postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | PostgreSQL database | TypeScript | Database queries |
| [sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) | SQLite database | TypeScript | Local database access |
| [google-drive](https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive) | Google Drive integration | TypeScript | Drive file access |
| [slack](https://github.com/modelcontextprotocol/servers/tree/main/src/slack) | Slack workspace | TypeScript | Channel/message access |
| [puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) | Browser automation | TypeScript | Web scraping |

### Community Servers

- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) - Curated list of community servers
- [MCP Server Registry](https://mcp-servers.org) - Searchable registry of public servers
- Community Discord for sharing and discovering servers

### Building Your Own

**When to build a custom server:**
- Connect to proprietary APIs or internal tools
- Create domain-specific integrations
- Combine multiple data sources
- Add specialized functionality

**Server Development Resources:**
- [Server Development Guide](https://modelcontextprotocol.io/docs/building-servers)
- [SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [Testing Guide](https://modelcontextprotocol.io/docs/testing)

## Client Implementations

### Desktop Applications

- **[Claude Desktop](https://claude.ai/download)** - Official Anthropic client
  - Native MCP support
  - Easy configuration
  - Best for beginners

- **[Continue.dev](https://continue.dev)** - VS Code/JetBrains extension
  - MCP server integration
  - IDE-native experience
  - Developer-focused

### Web Applications

- Custom web clients using MCP SDK
- Browser extension implementations
- Cloud-based MCP clients

### CLI Tools

- [mcp-cli](https://github.com/modelcontextprotocol/cli) - Command-line MCP client
- Custom CLI implementations
- Testing and debugging tools

### Building Your Own Client

- [Client Development Guide](https://modelcontextprotocol.io/docs/building-clients)
- [Client SDK](https://github.com/modelcontextprotocol/sdk)
- Example client implementations

## Tools & Libraries

### Official SDKs

- **[@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)** (TypeScript/JavaScript)
  - Full protocol implementation
  - Server and client support
  - Well-documented and maintained

- **[mcp](https://pypi.org/project/mcp/)** (Python)
  - Pythonic API
  - Async/await support
  - Popular for data science use cases

### Development Tools

- **MCP Inspector** - Debug and test MCP servers
- **MCP Validator** - Validate protocol compliance
- **Server Templates** - Starter templates for quick setup

### Testing Tools

- Unit testing frameworks for MCP servers
- Integration test helpers
- Mock client implementations

### Utilities

- Configuration generators
- Log analyzers
- Performance profilers

## Community Resources

### Forums & Discussion

- [MCP Discord Server](https://discord.gg/anthropic) - Active community chat
- [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions) - Technical discussions
- [Reddit r/ClaudeAI](https://reddit.com/r/ClaudeAI) - Community forum
- [Stack Overflow](https://stackoverflow.com/questions/tagged/model-context-protocol) - Q&A tagged with MCP

### Blogs & Articles

- [Anthropic Blog](https://www.anthropic.com/news) - Official announcements
- Community blog posts and tutorials
- Case studies and implementation stories

### Social Media

- [Twitter/X #ModelContextProtocol](https://twitter.com/search?q=%23ModelContextProtocol)
- LinkedIn groups and discussions
- YouTube channels covering MCP

### Contributing

- [Contributing Guide](https://github.com/modelcontextprotocol/specification/blob/main/CONTRIBUTING.md)
- How to submit new servers
- Documentation improvements
- Bug reports and feature requests

## Best Practices

### Security

- **Never expose sensitive credentials** in server code
- Use environment variables for API keys
- Implement proper authentication/authorization
- Validate all inputs from LLM tool calls
- Follow principle of least privilege
- Regularly update dependencies

### Performance

- Cache frequently accessed data
- Use streaming for large responses
- Implement request timeouts
- Handle concurrent requests efficiently
- Monitor resource usage

### Error Handling

- Provide clear error messages
- Log errors for debugging
- Graceful degradation when services unavailable
- User-friendly error responses to LLMs

### Testing

- Unit test individual tools and resources
- Integration test full server workflows
- Test error scenarios
- Validate protocol compliance
- Performance/load testing for production

### Documentation

- Document all tools with clear descriptions
- Provide usage examples
- Keep README up to date
- Document configuration options
- Include troubleshooting section

### Deployment

- Use process managers (PM2, systemd)
- Implement health checks
- Set up monitoring and alerting
- Plan for graceful shutdowns
- Version your servers

## Getting Help

### Troubleshooting

Common issues and solutions:

1. **Server not appearing in Claude Desktop**
   - Check configuration file syntax
   - Verify file paths are absolute
   - Restart Claude Desktop completely
   - Check server logs for errors

2. **Tools not being called**
   - Verify tool descriptions are clear
   - Check input schema is correct
   - Test server independently
   - Review Claude Desktop logs

3. **Connection errors**
   - Ensure server uses stdio correctly
   - Check for port conflicts (if using HTTP)
   - Verify permissions on files/directories
   - Test with MCP Inspector

### Resources for Help

- Official documentation
- GitHub issues for bug reports
- Discord community for quick questions
- Stack Overflow for detailed problems

## Contributing to This List

Found a great MCP resource? Want to add your server to the list?

1. Fork this repository
2. Add your resource in the appropriate section
3. Ensure links are working
4. Submit a pull request
5. Follow the existing format

### Criteria for Inclusion

- Must be MCP-related
- Working and maintained
- Clear documentation
- Adds value to learners

## License

This list is licensed under [CC0 1.0 Universal](LICENSE) - feel free to use and share!

## Acknowledgments

- Anthropic for creating MCP
- All contributors to MCP servers and tools
- Community members sharing knowledge and examples

---

**Note**: MCP is actively evolving. This guide is maintained as a community resource and may not reflect the very latest changes. Always refer to the [official documentation](https://modelcontextprotocol.io) for the most current information.

**Last Updated**: February 2026
