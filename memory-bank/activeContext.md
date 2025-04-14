# Active Context: MCP Server Development Assistant

## Current Focus

- **Phase 1: Local Documentation Cache Setup and Basic Access.**
- The immediate goal is to establish the local storage structure (`data/` directory with `structure.json` and `.md` files), manually populate it with initial content and structure, and implement the core MCP functionalities (`get_docs_structure` tool and dynamic resource access) to serve this local data.

## Recent Changes & Decisions

- Established the core Memory Bank structure and `.clinerules`.
- Confirmed the use of Python and the `mcp` library (`FastMCP`).
- **Revised Plan:** Instead of manually creating `structure.json`, we created a Python script (`scripts/scrape_structure.py`) to automatically scrape the documentation structure from `modelcontextprotocol.io`.
- Added `requests` and `beautifulsoup4` dependencies to `pyproject.toml` and installed them using `uv pip install`.
- Successfully executed `scripts/scrape_structure.py` to generate `data/structure.json`.
- Identified the existing `server.py` as the starting point for implementation.
- Updated `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md` previously to reflect the initial plan. *Note: These might need minor updates later to reflect the scraper approach.*

## Next Steps (Phase 1 Implementation - Revised)

1.  **Create `data/` Directory Structure:** Create the main `data/` directory and any necessary subdirectories based on the structure defined in the *generated* `data/structure.json` (e.g., `data/concepts`, `data/tutorials`, `data/quickstart`). *(This step might be partially done already based on file list)*.
2.  **Populate Content Files:** Manually create and populate the initial Markdown (`.md`) files within the `data/` directory structure, corresponding to the paths defined in `data/structure.json` (e.g., `data/introduction.md`, `data/concepts/tools.md`). Start with key pages like Introduction, Quickstart pages, Concepts overview, etc.
3.  **Implement `get_docs_structure` Tool:** Modify `server.py`:
    - Remove existing example code (if any).
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

- **Scraper Robustness:** The `scripts/scrape_structure.py` script depends on the website's current HTML structure. Future website changes might break the script.
- **Manual Population Scope:** Decide which key pages are essential to populate manually for Phase 1.
- **Dynamic Resource Implementation:** Determine the best way to implement dynamic resource handling within `FastMCP` (e.g., overriding methods, using FastAPI's routing directly if accessible).
- **Error Handling:** Implement robust error handling for file not found (in resources) and potential JSON parsing errors (in the tool).

## Important Patterns & Preferences

- Use `@mcp.tool` decorator for the `get_docs_structure` tool.
- Implement dynamic resource handling logic carefully, ensuring correct mapping from URI path to file path.
- Maintain consistency between `structure.json` paths and the actual file paths in the `data/` directory.
- Resource URIs should follow the pattern `mcp://docs/<path-from-structure.json>`.
- Adhere to Python type hinting as specified in `.clinerules`.
