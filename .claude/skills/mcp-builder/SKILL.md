---
name: mcp-builder
description: Build new MCP servers using FastMCP pattern with minimal token overhead for LearnFlow AI agents
triggers:
  - "build mcp server"
  - "create mcp tool"
  - "new mcp server"
  - "add mcp context"
  - "mcp fastmcp"
---

# MCP Builder

## When to Use
- Adding a new data source as an MCP tool for AI agents
- Wrapping an existing API as an MCP server
- Extending LearnFlow's AI context capabilities
- Building agent-callable tools for student/teacher data

## Instructions

1. Scaffold new MCP server:
   ```bash
   python scripts/scaffold.py --name <tool-name> --port <port>
   ```

2. Implement tool functions:
   ```bash
   # Edit the generated server file
   # Each @mcp.tool() function = one agent tool
   ```

3. Test the MCP server:
   ```bash
   python scripts/test_mcp.py --server <tool-name>
   ```

4. Register with LearnFlow agents:
   ```bash
   python scripts/register.py --server <tool-name>
   ```

## MCP Tool Pattern
```python
from fastmcp import FastMCP

mcp = FastMCP("my-tool")

@mcp.tool()
def get_data(query: str) -> str:
    """Get data — returns minimal string result."""
    result = fetch_and_filter(query)
    return f"✓ {len(result)} items found"  # ~10 tokens
```

## Validation
- [ ] MCP server responds to /tools endpoint
- [ ] Each tool returns < 100 tokens
- [ ] Server registered in Claude/Goose config

See [REFERENCE.md](./REFERENCE.md) for FastMCP patterns and SSE transport setup.
