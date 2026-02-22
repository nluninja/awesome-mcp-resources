#!/usr/bin/env node
/**
 * Calculator MCP Server Example - TypeScript
 * ===========================================
 *
 * An MCP server with multiple tools for basic arithmetic operations.
 * Demonstrates multiple tools, input validation, and error handling.
 *
 * Features:
 * - Add, subtract, multiply, divide
 * - Input validation
 * - Error handling (division by zero)
 * - Multiple tools in one server
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

/**
 * Common interface for arithmetic operations
 */
interface ArithmeticArgs {
  a: number;
  b: number;
}

/**
 * Create the MCP server
 */
const server = new Server(
  {
    name: "calculator-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Define the calculation tools
 */
const tools: Tool[] = [
  {
    name: "add",
    description: "Add two numbers together",
    inputSchema: {
      type: "object",
      properties: {
        a: { type: "number", description: "First number" },
        b: { type: "number", description: "Second number" },
      },
      required: ["a", "b"],
    },
  },
  {
    name: "subtract",
    description: "Subtract second number from first number",
    inputSchema: {
      type: "object",
      properties: {
        a: { type: "number", description: "Number to subtract from" },
        b: { type: "number", description: "Number to subtract" },
      },
      required: ["a", "b"],
    },
  },
  {
    name: "multiply",
    description: "Multiply two numbers",
    inputSchema: {
      type: "object",
      properties: {
        a: { type: "number", description: "First number" },
        b: { type: "number", description: "Second number" },
      },
      required: ["a", "b"],
    },
  },
  {
    name: "divide",
    description: "Divide first number by second number",
    inputSchema: {
      type: "object",
      properties: {
        a: { type: "number", description: "Numerator" },
        b: { type: "number", description: "Denominator" },
      },
      required: ["a", "b"],
    },
  },
];

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

/**
 * Handle tool execution
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const { a, b } = args as ArithmeticArgs;

  // Validate inputs are numbers
  if (typeof a !== "number" || typeof b !== "number") {
    throw new Error("Both arguments must be numbers");
  }

  let result: number;
  let operation: string;

  switch (name) {
    case "add":
      result = a + b;
      operation = `${a} + ${b}`;
      break;

    case "subtract":
      result = a - b;
      operation = `${a} - ${b}`;
      break;

    case "multiply":
      result = a * b;
      operation = `${a} × ${b}`;
      break;

    case "divide":
      if (b === 0) {
        return {
          content: [
            {
              type: "text",
              text: "Error: Cannot divide by zero",
            },
          ],
          isError: true,
        };
      }
      result = a / b;
      operation = `${a} ÷ ${b}`;
      break;

    default:
      throw new Error(`Unknown tool: ${name}`);
  }

  return {
    content: [
      {
        type: "text",
        text: `${operation} = ${result}`,
      },
    ],
  };
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Calculator MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
