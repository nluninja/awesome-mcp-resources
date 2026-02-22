# Awesome MCP Resources

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-blue)](https://modelcontextprotocol.io)
[![GitHub](https://img.shields.io/badge/GitHub-awesome--mcp--resources-181717?logo=github)](https://github.com/yourusername/awesome-mcp-resources)

> A curated list of resources for learning and working with Model Context Protocol (MCP) - a practical guide for students and developers to get started quickly.

## 🚀 Quick Navigation

- **New to MCP?** → Start with [Getting Started Guide](GETTING_STARTED.md) (30 minutes)
- **Want to see code?** → Browse [Examples](examples/)
- **Need quick reference?** → Check [Quick Reference](QUICKREF.md)
- **Looking for resources?** → Keep reading below ⬇️

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
- **MCP Clients**: Applications that connect to MCP servers (e.g., Claude Desktop, Continue.dev, custom implementations)
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
- An MCP-compatible client for testing (see [Client Implementations](#client-implementations))

### 5-Minute Setup

1. **Choose an MCP client** (to test your servers)
   - **Claude Desktop**: User-friendly, download from [claude.ai/download](https://claude.ai/download)
   - **Continue.dev**: IDE extension for VS Code/JetBrains
   - **MCP Inspector**: CLI testing tool - `npx @modelcontextprotocol/inspector`
   - **Custom client**: Build your own using the MCP SDK

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

3. **Test your server** using one of these methods:

   **Option A: Using MCP Inspector (CLI tool)**
   ```bash
   npx @modelcontextprotocol/inspector python /path/to/server.py
   ```

   **Option B: Using Claude Desktop**

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
   Restart Claude Desktop to load the server.

   **Option C: Using Continue.dev**

   Add to your Continue config (`~/.continue/config.json`):
   ```json
   {
     "mcpServers": [
       {
         "name": "my-first-server",
         "command": "python",
         "args": ["/path/to/server.py"]
       }
     ]
   }
   ```

   **Option D: Build your own client**

   Use the MCP SDK to create a custom client - see [Client Development Guide](https://modelcontextprotocol.io/docs/building-clients)

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

### Official Videos

- **[Anthropic MCP Announcement](https://www.youtube.com/c/anthropic-ai)** - Official launch video
- **[MCP Documentation Videos](https://modelcontextprotocol.io)** - Official tutorials

### Conference Talks & Presentations

- **[AI Engineer Summit 2024](https://www.ai.engineer/summit)** - MCP integration talks
  - Search: [AI Engineer + MCP on YouTube](https://www.youtube.com/results?search_query=AI+Engineer+Summit+Model+Context+Protocol)
- **[GitHub Universe 2024](https://githubuniverse.com/)** - AI tooling presentations
- **[PyCon Talks](https://www.youtube.com/@PyConUS)** - Python MCP implementations
- **[JSConf Talks](https://www.youtube.com/results?search_query=jsconf+llm+integration)** - JavaScript AI integrations
- **Conference Playlist**: [MCP Conference Talks](https://www.youtube.com/results?search_query=model+context+protocol+conference)

### Tutorial Videos

- **[What is Model Context Protocol?](https://www.youtube.com/results?search_query=what+is+model+context+protocol+tutorial)** - Introductory overviews
- **[Building Your First MCP Server](https://www.youtube.com/results?search_query=building+mcp+server+tutorial)** - Step-by-step tutorials
- **[MCP Server Development](https://www.youtube.com/results?search_query=mcp+server+development)** - Advanced techniques
- **[MCP with Python](https://www.youtube.com/results?search_query=model+context+protocol+python)** - Python-specific tutorials
- **[MCP with TypeScript](https://www.youtube.com/results?search_query=model+context+protocol+typescript)** - TypeScript implementations

### Live Coding & Demos

- **[MCP Live Coding Sessions](https://www.youtube.com/results?search_query=model+context+protocol+live+coding)**
- **[Building AI Agents with MCP](https://www.youtube.com/results?search_query=building+ai+agents+mcp)**
- **[MCP Integration Examples](https://www.youtube.com/results?search_query=mcp+integration+demo)**

### Community Channels

- **[Simon Willison](https://www.youtube.com/@simonw)** - AI and LLM content including MCP
- **[Matt Pocock](https://www.youtube.com/@mattpocockuk)** - TypeScript and AI tooling
- **[Fireship](https://www.youtube.com/@Fireship)** - Quick tech explainers
- **[Theo - t3.gg](https://www.youtube.com/@t3dotgg)** - Web dev and AI

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

MCP clients connect to MCP servers and enable LLMs to use the exposed tools and resources.

### Desktop Applications

- **[Claude Desktop](https://claude.ai/download)** - Official Anthropic client
  - Platform: macOS, Windows
  - Native MCP support
  - Simple JSON configuration
  - Best for: Beginners, general use
  - [Setup Guide](https://modelcontextprotocol.io/quickstart)

- **[Continue.dev](https://continue.dev)** - IDE extension
  - Platform: VS Code, JetBrains IDEs
  - MCP server integration
  - Code-aware context
  - Best for: Developers, coding workflows
  - [MCP Configuration](https://docs.continue.dev/features/mcp)

### CLI Tools

- **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** - Debugging tool
  - Test and debug MCP servers
  - Interactive interface
  - Protocol inspection
  - Best for: Server development
  - Install: `npx @modelcontextprotocol/inspector`

- **Custom CLI clients** - Build your own
  - Use MCP SDK
  - Scriptable automation
  - Custom workflows

### Web & Browser

- **Web-based clients** - Using MCP SDK
  - Browser-based interfaces
  - Cloud-hosted clients
  - Custom dashboards

- **Browser extensions** - Community implementations
  - Direct browser integration
  - Bookmarklet tools

### Agent Frameworks

- **[LangChain](https://www.langchain.com/)** - MCP integration
  - Use MCP servers as LangChain tools
  - Agent orchestration
  - [Integration guide](https://python.langchain.com/docs/integrations/tools/)

- **[LlamaIndex](https://www.llamaindex.ai/)** - Data framework
  - MCP as data sources
  - Retrieval augmentation

- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** - Autonomous agents
  - MCP tool integration
  - Multi-step reasoning

### Building Your Own Client

**Why build a custom client:**
- Integrate MCP into existing applications
- Create specialized workflows
- Custom UI/UX requirements
- Specific security/compliance needs

**Resources:**
- **[Client Development Guide](https://modelcontextprotocol.io/docs/building-clients)** - Official guide
- **[TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)** - Client implementation
- **[Python SDK](https://github.com/modelcontextprotocol/python-sdk)** - Python client tools
- **[Example Clients](https://github.com/modelcontextprotocol/specification/tree/main/examples)** - Reference implementations

**Basic client structure:**
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "python",
  args: ["server.py"]
});

const client = new Client({
  name: "my-client",
  version: "1.0.0"
});

await client.connect(transport);

// List available tools
const tools = await client.listTools();

// Call a tool
const result = await client.callTool({
  name: "tool_name",
  arguments: { param: "value" }
});
```

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

- **[Anthropic Discord](https://discord.gg/anthropic)** - Official Discord server with #mcp channel
- **[MCP GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)** - Technical discussions and Q&A
- **[Reddit r/ClaudeAI](https://reddit.com/r/ClaudeAI)** - Community forum with MCP discussions
- **[Reddit r/ModelContextProtocol](https://reddit.com/r/ModelContextProtocol)** - Dedicated MCP subreddit
- **[Stack Overflow - MCP Tag](https://stackoverflow.com/questions/tagged/model-context-protocol)** - Technical Q&A

### Conferences & Talks

- **[AI Engineer Summit](https://www.ai.engineer/)** - Annual conference featuring MCP presentations
- **[Anthropic MCP Launch Event](https://www.anthropic.com/news/model-context-protocol)** - Original announcement (November 2024)
- **[GitHub Universe](https://githubuniverse.com/)** - Developer conference with AI/LLM tracks
- **[PyCon](https://pycon.org/)** - Python conference with AI integration talks
- **[JSConf](https://jsconf.com/)** - JavaScript conference featuring AI tooling
- **Conference recordings on [YouTube](https://www.youtube.com/results?search_query=model+context+protocol+conference)**

### Blogs & Articles

- **[Anthropic Blog](https://www.anthropic.com/news)** - Official announcements and updates
- **[MCP on Dev.to](https://dev.to/t/mcp)** - Community articles and tutorials
- **[MCP on Medium](https://medium.com/search?q=model%20context%20protocol)** - Technical deep dives
- **[Hacker News - MCP discussions](https://hn.algolia.com/?q=model+context+protocol)** - Community discussions
- **[Simon Willison's Blog](https://simonwillison.net/)** - AI and MCP insights

### Social Media

- **[Twitter/X #ModelContextProtocol](https://twitter.com/search?q=%23ModelContextProtocol)** - Latest updates and discussions
- **[Twitter/X @AnthropicAI](https://twitter.com/AnthropicAI)** - Official Anthropic account
- **[LinkedIn MCP Group](https://www.linkedin.com/search/results/groups/?keywords=model%20context%20protocol)** - Professional network
- **[YouTube MCP Channel](https://www.youtube.com/results?search_query=model+context+protocol)** - Video tutorials and talks

### Open Source Community

- **[MCP GitHub Organization](https://github.com/modelcontextprotocol)** - Official repositories
  - [Specification](https://github.com/modelcontextprotocol/specification) - Protocol spec
  - [SDKs](https://github.com/modelcontextprotocol/sdk) - Official SDKs
  - [Servers](https://github.com/modelcontextprotocol/servers) - Reference implementations
- **[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)** - Community server collection
- **[MCP Examples](https://github.com/topics/mcp-server)** - GitHub topic for MCP servers

### Contributing

- **[Contributing Guide](https://github.com/modelcontextprotocol/specification/blob/main/CONTRIBUTING.md)** - How to contribute
- **[Good First Issues](https://github.com/search?q=org%3Amodelcontextprotocol+label%3A%22good+first+issue%22&type=issues)** - Beginner-friendly contributions
- **[Documentation](https://github.com/modelcontextprotocol/specification/tree/main/docs)** - Help improve docs
- **[Server Registry](https://github.com/modelcontextprotocol/servers/discussions)** - Submit your servers

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

1. **Server not being detected by client**
   - Check configuration file syntax (JSON must be valid)
   - Verify file paths are absolute, not relative
   - Restart your MCP client completely
   - Check server logs for initialization errors
   - Test with MCP Inspector: `npx @modelcontextprotocol/inspector python server.py`

2. **Tools not being called**
   - Verify tool descriptions are clear and specific
   - Check input schema is valid JSON Schema
   - Test server independently from command line
   - Review client logs for errors
   - Use MCP Inspector to debug tool definitions

3. **Connection errors**
   - Ensure server uses correct transport (stdio is default)
   - Check for port conflicts (if using HTTP/WebSocket)
   - Verify permissions on files/directories
   - Confirm server process is actually running
   - Test with: `echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | python server.py`

4. **Import/dependency errors**
   - Verify all dependencies are installed
   - Check virtual environment is activated (Python)
   - Ensure Node.js modules are in node_modules (TypeScript)
   - Review Python path / Node path configuration

### Resources for Help

- **[Official Documentation](https://modelcontextprotocol.io)** - Comprehensive guides
- **[GitHub Issues](https://github.com/modelcontextprotocol/specification/issues)** - Bug reports
- **[Discord Community](https://discord.gg/anthropic)** - Quick questions (#mcp channel)
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/model-context-protocol)** - Detailed Q&A
- **[GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)** - Technical discussions

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
