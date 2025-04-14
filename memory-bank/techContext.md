# Technical Context: MCP Server Development Assistant

## Core Technology Stack

- **Language:** Python (Version >= 3.12, as specified in `pyproject.toml`)
- **MCP Framework:** `mcp` Python library (Version >= 1.6.0), specifically using the `FastMCP` class which is built on FastAPI.
- **Primary Dependency:** `mcp[cli]`

## Development Environment

- **Package Management:** Using `uv` (implied by `uv.lock`) and `pyproject.toml` for dependency management.
- **Server Execution:** The server can be run directly using `python server.py` due to the `if __name__ == "__main__": mcp.run()` block in `server.py`. Alternatively, the `mcp` CLI might offer other ways to run/manage the server.

## Key Libraries & Modules Used

- `mcp.server.fastmcp.FastMCP`: The core class for creating the MCP server instance.
- `mcp.server.fastmcp.Context`: Used within tool implementations to access request context and logging utilities (like `ctx.info`).
- Decorators (`@mcp.resource`, `@mcp.tool`, `@mcp.prompt`): The primary mechanism for defining MCP resources, tools, and prompts within the `FastMCP` framework.
- `mcp.server.fastmcp.prompts.base`: Contains base classes for defining prompt messages (e.g., `UserMessage`, `AssistantMessage`).

## Data Storage Approach

- **Confirmed Plan:** Store documentation content in local Markdown files (`.md`) within a `data/` directory, organized in subdirectories mirroring the website structure.
- **Hierarchy Storage:** Store the documentation's hierarchical structure (navigation) in a dedicated JSON file: `data/structure.json`.

## Tool and Resource Implementation Patterns

- **Structure Tool:** Implement a specific tool `get_docs_structure` using the `@mcp.tool` decorator. This tool will read and return the content of `data/structure.json`.
- **Dynamic Resources:** Implement resource access dynamically. The server will likely need a mechanism (potentially overriding a method in `FastMCP` or using a catch-all route if supported) to handle resource requests like `mcp://docs/...`. This handler will:
    - Parse the path from the URI.
    - Construct the corresponding local file path within the `data/` directory (e.g., `data/concepts/tools.md`).
    - Read the file content and return it.
    - Include error handling for missing files.
- **Standard Decorators:** Continue using `@mcp.tool` for defined tools. Resource definition might deviate from simple `@mcp.resource` decorators due to the dynamic nature.

## Potential Future Dependencies (for Update Tool)

- `requests`: For fetching web pages.
- `beautifulsoup4` or similar: For parsing HTML content during scraping.
