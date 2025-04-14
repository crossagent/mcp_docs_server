# Active Context: MCP Server Development Assistant

## Current Focus

- **Phase 1: Local Documentation Cache Setup and Basic Access.**
- The immediate goal is to establish the local storage structure (`data/` directory with `structure.json` and `.md` files), manually populate it with initial content and structure, and implement the core MCP functionalities (`get_docs_structure` tool and dynamic resource access) to serve this local data.

## Recent Changes & Decisions

- Established the core Memory Bank structure and `.clinerules`.
- Confirmed the use of Python and the `mcp` library (`FastMCP`).
- **Finalized Plan:** Use local storage (`data/` directory) for both documentation structure (`structure.json`) and content (`.md` files). Access will be provided via an MCP tool (`get_docs_structure`) and dynamic MCP resources mapping URIs to local files. Manual population initially, with a future plan for an automated update tool.
- Identified the existing `server.py` as the starting point for implementation.
- Updated `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md` to reflect the finalized plan.

## Next Steps (Phase 1 Implementation)

1.  **Create `data/` Directory Structure:** Create the main `data/` directory and any necessary subdirectories based on the website's navigation structure (e.g., `data/concepts`, `data/tutorials`).
2.  **Create `structure.json`:** Create the `data/structure.json` file. Manually populate it with the hierarchical structure derived from the `modelcontextprotocol.io` website's navigation sidebar. Define the `title` and `path` for each entry.
3.  **Populate Content Files:** Manually create and populate the initial Markdown (`.md`) files within the `data/` directory structure, corresponding to the paths defined in `structure.json` (e.g., `data/introduction.md`, `data/concepts/tools.md`). Start with key pages like Introduction, Quickstart, Concepts overview, etc.
4.  **Implement `get_docs_structure` Tool:** Modify `server.py`:
    - Remove existing example code.
    - Implement the `get_docs_structure` tool using `@mcp.tool` to read and return the content of `data/structure.json`.
5.  **Implement Dynamic Resource Handling:** Modify `server.py`:
    - Implement the logic to handle resource requests like `mcp://docs/...`.
    - Parse the requested path from the URI.
    - Construct the full path to the corresponding `.md` file within `data/`.
    - Read the file content and return it, including error handling for missing files.
6.  **Testing:** Run the server (`python server.py`) and use an MCP client to:
    - Call `get_docs_structure` and verify the returned JSON structure.
    - Access various resources using URIs derived from the structure (e.g., `mcp://docs/introduction`, `mcp://docs/concepts/tools`) and verify the correct Markdown content is returned.

## Active Considerations & Questions

- **`structure.json` Format:** Ensure a consistent and useful format for `structure.json` (e.g., nested objects with `title` and `path` keys).
- **Manual Population Scope:** Decide which key pages are essential to populate manually for Phase 1.
- **Dynamic Resource Implementation:** Determine the best way to implement dynamic resource handling within `FastMCP` (e.g., overriding methods, using FastAPI's routing directly if accessible).
- **Error Handling:** Implement robust error handling for file not found (in resources) and potential JSON parsing errors (in the tool).

## Important Patterns & Preferences

- Use `@mcp.tool` decorator for the `get_docs_structure` tool.
- Implement dynamic resource handling logic carefully, ensuring correct mapping from URI path to file path.
- Maintain consistency between `structure.json` paths and the actual file paths in the `data/` directory.
- Resource URIs should follow the pattern `mcp://docs/<path-from-structure.json>`.
- Adhere to Python type hinting as specified in `.clinerules`.
