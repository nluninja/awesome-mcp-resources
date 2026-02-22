#!/usr/bin/env python3
"""
Notes MCP Server Example - Python
==================================

An MCP server that manages simple text notes using the file system.
Demonstrates resources and tools working together.

Features:
- List all notes (resource)
- Read specific notes (resource)
- Create new notes (tool)
- Delete notes (tool)

Usage:
    python notes_server.py
"""

import asyncio
import os
from pathlib import Path
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent


# Create server instance
app = Server("notes-server")

# Directory to store notes (in user's home directory)
NOTES_DIR = Path.home() / ".mcp_notes"
NOTES_DIR.mkdir(exist_ok=True)


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available notes as resources.

    Resources are data sources that the LLM can read from.
    Each note file becomes a resource.
    """
    resources = []

    # List all .txt files in the notes directory
    for note_file in NOTES_DIR.glob("*.txt"):
        resources.append(
            Resource(
                uri=f"note:///{note_file.stem}",
                name=f"Note: {note_file.stem}",
                description=f"A text note named '{note_file.stem}'",
                mimeType="text/plain"
            )
        )

    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read the content of a specific note.

    Args:
        uri: Resource URI in format "note:///name"

    Returns:
        The content of the note
    """
    # Extract note name from URI
    if not uri.startswith("note:///"):
        raise ValueError(f"Invalid note URI: {uri}")

    note_name = uri[8:]  # Remove "note:///" prefix
    note_file = NOTES_DIR / f"{note_name}.txt"

    if not note_file.exists():
        raise FileNotFoundError(f"Note '{note_name}' not found")

    return note_file.read_text()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Define tools for creating and managing notes."""
    return [
        Tool(
            name="create_note",
            description="Create a new note with the given name and content",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the note (without .txt extension)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the note"
                    }
                },
                "required": ["name", "content"]
            }
        ),
        Tool(
            name="delete_note",
            description="Delete an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the note to delete"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="list_notes",
            description="List all available notes",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution."""

    if name == "create_note":
        note_name = arguments["name"]
        content = arguments["content"]

        # Sanitize filename
        safe_name = "".join(c for c in note_name if c.isalnum() or c in (' ', '-', '_'))
        note_file = NOTES_DIR / f"{safe_name}.txt"

        # Write the note
        note_file.write_text(content)

        return [TextContent(
            type="text",
            text=f"Note '{safe_name}' created successfully!"
        )]

    elif name == "delete_note":
        note_name = arguments["name"]
        note_file = NOTES_DIR / f"{note_name}.txt"

        if not note_file.exists():
            return [TextContent(
                type="text",
                text=f"Note '{note_name}' not found."
            )]

        note_file.unlink()
        return [TextContent(
            type="text",
            text=f"Note '{note_name}' deleted successfully!"
        )]

    elif name == "list_notes":
        notes = [f.stem for f in NOTES_DIR.glob("*.txt")]

        if not notes:
            return [TextContent(type="text", text="No notes found.")]

        notes_list = "\n".join(f"- {note}" for note in sorted(notes))
        return [TextContent(
            type="text",
            text=f"Available notes:\n{notes_list}"
        )]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Start the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        init_options = app.create_initialization_options()
        await app.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
