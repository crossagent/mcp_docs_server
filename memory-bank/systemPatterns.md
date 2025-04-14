# System Patterns: MCP Server Development Assistant

## Core Architecture

The system will be a Python-based MCP Server. It will likely use a framework suitable for building web services (like Flask or FastAPI) as the underlying engine, upon which the MCP server logic will be built.

## Data Storage and Structure

- **Source:** Content and structure derived from [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/). Initially populated manually, with plans for future automated updates.
- **Storage Location:** A dedicated `data/` directory within the project root.
- **Content Storage:** Documentation content for each section will be stored as individual Markdown files (`.md`) within the `data/` directory, potentially organized into subdirectories mirroring the website's structure (e.g., `data/concepts/tools.md`).
- **Structure Storage:** The hierarchical structure of the documentation (matching the website's navigation) will be stored in a JSON file, `data/structure.json`. This file maps navigation titles to content file paths.
- **Decision:** Use local Markdown files for content and a local JSON file (`structure.json`) for the hierarchy. This provides reliable local access and clear separation of structure and content.

## MCP Implementation

- **Server Logic:** Implement the core MCP server interface using the `FastMCP` framework.
- **Structure Discovery Tool:**
    - Implement an MCP Tool named `get_docs_structure`.
    - This tool will read the `data/structure.json` file and return its content (likely as a JSON string or Python object representation) to the client.
- **Dynamic Resource Provision:**
    - Implement a dynamic resource handling mechanism. Instead of defining one resource per file, the server will accept resource URIs following a pattern (e.g., `mcp://docs/...`).
    - The `access_resource` implementation will parse the requested URI path (e.g., `/concepts/tools` from `mcp://docs/concepts/tools`).
    - It will map this path to the corresponding local Markdown file (e.g., `data/concepts/tools.md`).
    - It will read the content of the Markdown file and return it. Error handling for missing files will be included.
- **(Future) Update Tool:**
    - Plan to implement an MCP Tool `trigger_docs_update` in a later phase to automate the refreshing of `data/structure.json` and the `.md` files from the live website.

## Key Technical Decisions (Initial)

- **Language:** Python (as indicated by the existing `server.py`, `pyproject.toml`).
- **Web Framework:** FastAPI (via `FastMCP` from the `mcp` library).
- **Data Storage:** Local Markdown files (`.md`) for content and a JSON file (`structure.json`) for hierarchy within the `data/` directory.
- **MCP Library:** Confirmed use of the official Python `mcp` library (`mcp[cli]>=1.6.0`).

## Future Considerations

- **Automated Content Updates:** Implement the `trigger_docs_update` tool and the associated scraping/updating logic.
- **Semantic Search:** Potentially integrate vector search capabilities for natural language queries against the documentation content.
