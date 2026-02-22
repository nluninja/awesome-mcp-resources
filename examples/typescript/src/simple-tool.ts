#!/usr/bin/env node
/**
 * Simple MCP Server Example - TypeScript
 * ========================================
 *
 * A minimal MCP server that exposes a single "greet" tool.
 * Perfect for understanding the basics of MCP server implementation in TypeScript.
 *
 * Usage:
 *   npm install
 *   npm run build
 *   node dist/simple-tool.js
 *
 * Configuration for Claude Desktop:
 * {
 *   "mcpServers": {
 *     "simple-tool": {
 *       "command": "node",
 *       "args": ["/absolute/path/to/dist/simple-tool.js"]
 *     }
 *   }
 * }
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

/**
 * Define the greet tool interface
 */
interface GreetArgs {
  name: string;
  formal?: boolean;
}

/**
 * Create the MCP server instance
 */
const server = new Server(
  {
    name: "simple-tool-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Handle the list_tools request
 * This tells the client what tools are available
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "greet",
        description: "Greet someone by name with a friendly message",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "The name of the person to greet",
            },
            formal: {
              type: "boolean",
              description: "Whether to use formal greeting",
              default: false,
            },
          },
          required: ["name"],
        },
      } as Tool,
    ],
  };
});

/**
 * Handle the call_tool request
 * This executes the requested tool with provided arguments
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "greet") {
    const { name: personName, formal = false } = args as GreetArgs;

    let greeting: string;
    if (formal) {
      greeting = `Good day, ${personName}. It's a pleasure to meet you.`;
    } else {
      greeting = `Hey ${personName}! Nice to meet you!`;
    }

    return {
      content: [
        {
          type: "text",
          text: greeting,
        },
      ],
    };
  }

  // Handle unknown tool
  throw new Error(`Unknown tool: ${name}`);
});

/**
 * Start the server
 */
async function main() {
  // Use stdio transport for communication
  const transport = new StdioServerTransport();

  // Connect the server to the transport
  await server.connect(transport);

  // Log to stderr (stdout is used for MCP communication)
  console.error("Simple Tool MCP Server running on stdio");
}

// Run the server
main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
