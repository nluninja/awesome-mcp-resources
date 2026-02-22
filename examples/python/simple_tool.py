#!/usr/bin/env python3
"""
Simple MCP Server Example - Python
===================================

This is a minimal MCP server that exposes a single "greet" tool.
Perfect for understanding the basics of MCP server implementation.

Usage:
    python simple_tool.py

Configuration for Claude Desktop:
    {
      "mcpServers": {
        "simple-tool": {
          "command": "python",
          "args": ["/absolute/path/to/simple_tool.py"]
        }
      }
    }
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create the MCP server instance
app = Server("simple-tool-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define the tools available to the LLM.

    This function is called by the MCP client to discover what tools
    this server provides.
    """
    return [
        Tool(
            name="greet",
            description="Greet someone by name with a friendly message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person to greet"
                    },
                    "formal": {
                        "type": "boolean",
                        "description": "Whether to use formal greeting",
                        "default": False
                    }
                },
                "required": ["name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool execution requests from the LLM.

    Args:
        name: The name of the tool being called
        arguments: Dictionary of arguments passed to the tool

    Returns:
        List of text content responses
    """
    if name == "greet":
        person_name = arguments.get("name", "friend")
        is_formal = arguments.get("formal", False)

        if is_formal:
            greeting = f"Good day, {person_name}. It's a pleasure to meet you."
        else:
            greeting = f"Hey {person_name}! Nice to meet you!"

        return [TextContent(type="text", text=greeting)]

    # Handle unknown tool
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """
    Main entry point - starts the MCP server with stdio transport.

    The stdio transport communicates via standard input/output,
    which is the most common way to run MCP servers.
    """
    # Use stdio for communication (standard for MCP servers)
    async with stdio_server() as (read_stream, write_stream):
        # Create initialization options
        init_options = app.create_initialization_options()

        # Run the server
        await app.run(
            read_stream,
            write_stream,
            init_options
        )


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
