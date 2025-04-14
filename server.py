# e:/mcp_docs_server/server.py
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union

from mcp import Resource # Resource seems ok here
# ResourceError not found, use standard Python exceptions
from mcp.server.fastmcp import Context, FastMCP

# --- Constants ---
DATA_DIR = Path(__file__).parent / "data"
STRUCTURE_FILE = DATA_DIR / "structure.json"
RESOURCE_PREFIX = "mcp://docs/"

# --- MCP Server Instance ---
mcp = FastMCP("MCPDocsAssistant")

# --- Tool: Get Documentation Structure ---
@mcp.tool()
def get_docs_structure(ctx: Context) -> Union[List[Dict[str, Any]], str]:
    """
    Retrieves the hierarchical structure of the locally cached MCP documentation.

    Returns:
        Union[List[Dict[str, Any]], str]: A list representing the nested structure
                                          of the documentation, or an error message string.
    """
    ctx.info(f"Attempting to read documentation structure from: {STRUCTURE_FILE}")
    if not STRUCTURE_FILE.is_file():
        ctx.error(f"Structure file not found: {STRUCTURE_FILE}")
        return f"Error: Documentation structure file not found at {STRUCTURE_FILE}"
    try:
        with open(STRUCTURE_FILE, "r", encoding="utf-8") as f:
            structure = json.load(f)
        ctx.info("Successfully loaded documentation structure.")
        return structure
    except json.JSONDecodeError as e:
        ctx.error(f"Error decoding JSON from {STRUCTURE_FILE}: {e}")
        return f"Error: Could not decode structure file {STRUCTURE_FILE}. Invalid JSON."
    except Exception as e:
        ctx.error(f"An unexpected error occurred while reading {STRUCTURE_FILE}: {e}")
        return f"Error: An unexpected error occurred while reading the structure file."

# --- Static Resource Example (for testing listing) ---
@mcp.resource(f"{RESOURCE_PREFIX}introduction")
def get_introduction_statically() -> Resource:
    """Provides static access to the introduction file for testing."""
    doc_path = "introduction"
    full_uri = f"{RESOURCE_PREFIX}{doc_path}"
    file_path = (DATA_DIR / doc_path).with_suffix(".md")
    if not file_path.is_file():
        raise FileNotFoundError(f"Static resource file not found: {file_path}")
    try:
        content = file_path.read_text(encoding="utf-8")
        # Add the required 'name' parameter
        return Resource(name=doc_path, uri=full_uri, content=content, content_type="text/markdown")
    except Exception as e:
        # Simplified error handling for static example
        raise IOError(f"Could not read static resource file {file_path}: {e}")


# --- Dynamic Resource Access (Commented out for testing listing) ---
# # Use the @mcp.resource decorator with a simplified path parameter
# @mcp.resource(f"{RESOURCE_PREFIX}{{doc_path}}") # Removed :path
# def get_doc_content(doc_path: str) -> Resource: # Removed ctx: Context
#     """
#     Provides access to locally cached MCP documentation Markdown files
#     based on the path captured from the URI.
#     e.g., 'mcp://docs/concepts/tools' maps doc_path='concepts/tools'.
#     NOTE: This function cannot use the 'ctx' object due to library constraints.
#     """
#     full_uri = f"{RESOURCE_PREFIX}{doc_path}" # Reconstruct full URI for Resource object
#     # Logging removed as ctx is unavailable here
#     # print(f"Received resource request for path: {doc_path} (URI: {full_uri})") # Optional: Use print for basic debug
#
#     # Basic sanitization (already partially handled by path capture, but double-check)
#     if ".." in doc_path:
#          # Logging removed
#          raise ValueError("Invalid path characters requested.")
#
#     # Construct the full path to the markdown file
#     # Assume paths in structure.json don't have .md, so add it here
#     file_path = (DATA_DIR / doc_path).with_suffix(".md")
#     # Logging removed
#     # print(f"Attempting to access file at: {file_path}") # Optional: Use print for basic debug
#
#     # Check if the path resolves correctly and safely within DATA_DIR
#     try:
#         resolved_path = file_path.resolve(strict=True) # strict=True checks existence
#         if DATA_DIR.resolve() not in resolved_path.parents:
#              # Logging removed
#              raise ValueError("Access denied: Path traversal attempt.")
#     except FileNotFoundError:
#         # Logging removed
#         raise FileNotFoundError(f"Documentation file not found for path: {doc_path}")
#     except Exception as e: # Catches other potential resolution errors
#         # Logging removed
#         raise ValueError(f"Error resolving file path for: {doc_path}")
#
#     # Read and return the file content
#     try:
#         content = resolved_path.read_text(encoding="utf-8")
#         # Logging removed
#         # Return as a simple text resource
#         return Resource(uri=full_uri, content=content, content_type="text/markdown")
#     except IOError as e: # Catch specific IO errors during read
#         # Logging removed
#         raise IOError(f"Could not read documentation file for path: {doc_path}")
#     except Exception as e: # Catch any other unexpected errors during read
#         # Logging removed
#         raise Exception(f"Unexpected error reading documentation file for path: {doc_path}")


# --- Run Server ---
if __name__ == "__main__":
    print(f"Serving documentation from: {DATA_DIR.resolve()}")
    print(f"Using structure file: {STRUCTURE_FILE.resolve()}")
    print(f"Resource URI prefix: {RESOURCE_PREFIX}")
    mcp.run()
