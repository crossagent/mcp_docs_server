# e:/mcp_docs_server/server.py
import json
import os
import logging
import urllib.parse  # 添加这个导入
from pathlib import Path
from typing import Any, Dict, List, Union, Optional

from mcp import Resource
from mcp.server.fastmcp import Context, FastMCP

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mcp_docs_server.log')
    ]
)
logger = logging.getLogger('mcp_docs_server')

# --- Constants ---
DATA_DIR = Path(__file__).parent / "data"
STRUCTURE_FILE = DATA_DIR / "structure.json"
STRUCTURE_WITH_SUMMARIES_FILE = DATA_DIR / "structure_with_summaries.json"  # 添加新的结构文件路径
RESOURCE_PREFIX = "mcp://docs/"

# --- MCP Server Instance ---
mcp = FastMCP("MCPDocsAssistant")

# --- Document Structure Cache ---
_structure_cache = None

def get_doc_structure():
    """
    Load and cache the document structure from structure_with_summaries.json 
    or fall back to structure.json if not available.
    Returns the structure as a Python object.
    """
    global _structure_cache
    
    if _structure_cache is None:
        try:
            # 尝试优先读取带摘要的结构文件
            structure_file = STRUCTURE_WITH_SUMMARIES_FILE if STRUCTURE_WITH_SUMMARIES_FILE.exists() else STRUCTURE_FILE
            
            with open(structure_file, "r", encoding="utf-8") as f:
                _structure_cache = json.load(f)
                logger.info(f"Document structure loaded and cached from {structure_file.name}")
        except Exception as e:
            logger.error(f"Failed to load document structure: {str(e)}", exc_info=True)
            raise
            
    return _structure_cache

def find_doc_path(doc_name: str) -> Optional[str]:
    """
    Find the document path by its name in the structure.json.
    Performs case-insensitive search.
    
    Args:
        doc_name: The document name to search for
        
    Returns:
        The path if found, None otherwise
    """
    structure = get_doc_structure()
    # 转换为小写以支持大小写不敏感搜索
    doc_name_lower = doc_name.lower()
    
    def search_in_section(items):
        for item in items:
            # 使用小写比较来实现大小写不敏感搜索
            if "title" in item and item["title"].lower() == doc_name_lower and "path" in item:
                return item["path"]
                
            # Check children if they exist
            if "children" in item:
                result = search_in_section(item["children"])
                if result:
                    return result
        return None
    
    return search_in_section(structure)

# --- Structure Resource ---
@mcp.resource(f"{RESOURCE_PREFIX}structure")
def get_structure() -> Resource:
    """
    Provides document directory structure information with summaries.
    Returns a resource containing document titles and summaries that can be used with get_doc_content.
    Path information is intentionally removed from the returned structure.
    """
    try:
        structure = get_doc_structure()
        
        # 创建一个不包含 path 字段的结构副本
        def remove_paths(items):
            result = []
            for item in items:
                # 创建不带 path 的项目副本
                new_item = {k: v for k, v in item.items() if k != 'path'}
                
                # 处理子项目
                if "children" in item and isinstance(item["children"], list):
                    new_item["children"] = remove_paths(item["children"])
                    
                result.append(new_item)
            return result
        
        # 处理结构数据，移除 path 字段
        clean_structure = remove_paths(structure)
        
        # 添加额外信息
        result = {
            "structure": clean_structure,
            "description": "MCP Documentation Structure with Summaries",
            "usage": f"Documents can be accessed via '{RESOURCE_PREFIX}{{doc_name}}'"
        }
        
        content = json.dumps(result, ensure_ascii=False, indent=2)
        return Resource(
            name="structure", 
            uri=f"{RESOURCE_PREFIX}structure", 
            content=content, 
            content_type="application/json"
        )
    except Exception as e:
        error_msg = f"Error retrieving document structure: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg)

# --- Document Access By Name ---
@mcp.resource(f"{RESOURCE_PREFIX}{{doc_name}}") 
def get_doc_content(doc_name: str) -> Resource:
    """
    Provides access to documentation by document name.
    The document name should match a title in the structure.json file.
    Supports case-insensitive matching.
    """
    # 解码URL编码的字符，例如将 %20 转换为空格
    doc_name = urllib.parse.unquote(doc_name)
    
    logger.info(f"Received request for document: '{doc_name}' (case-insensitive search)")
    
    # Find the document path in structure.json (now with case-insensitive search)
    doc_path = find_doc_path(doc_name)
    if not doc_path:
        logger.error(f"Document not found: '{doc_name}' (case-insensitive search)")
        raise ValueError(f"Document '{doc_name}' not found in structure")
    
    # Remove leading slash if present
    if doc_path.startswith('/'):
        doc_path = doc_path[1:]
        logger.debug(f"Removed leading slash from path: {doc_path}")
    
    # Convert forward slashes to the platform-specific separator
    normalized_path = os.path.normpath(doc_path)
    logger.debug(f"Normalized path: {normalized_path}")
    
    # Split the path into components to handle platform-specific path construction
    path_components = normalized_path.split(os.path.sep)
    
    # Build the file path using proper platform-specific path joining
    file_path = DATA_DIR
    for component in path_components:
        if component:  # Skip empty components
            file_path = file_path / component
    
    # Add .md extension
    file_path = file_path.with_suffix(".md")
    logger.info(f"Resolved file path: {file_path}")

    # Check if the path resolves correctly and safely within DATA_DIR
    try:
        resolved_path = file_path.resolve(strict=True)  # strict=True checks existence
        if DATA_DIR.resolve() not in resolved_path.parents and DATA_DIR.resolve() != resolved_path:
            logger.warning(f"Access denied: Path traversal attempt for {doc_name}")
            raise ValueError("Access denied: Path traversal attempt.")
    except FileNotFoundError:
        logger.error(f"Documentation file not found: {file_path}")
        raise FileNotFoundError(f"Documentation file not found for document: {doc_name}")
    except Exception as e:
        logger.error(f"Error resolving file path for: {doc_name}", exc_info=True)
        raise ValueError(f"Error resolving file path for: {doc_name}")

    # Read and return the file content
    try:
        content = resolved_path.read_text(encoding="utf-8")
        logger.info(f"Successfully loaded content for: {doc_name}")
        return Resource(name=doc_name, uri=f"{RESOURCE_PREFIX}{doc_name}", content=content, content_type="text/markdown")
    except IOError:
        logger.error(f"Could not read file: {resolved_path}", exc_info=True)
        raise IOError(f"Could not read documentation file for document: {doc_name}")
    except Exception as e:
        logger.error(f"Unexpected error reading file: {resolved_path}", exc_info=True)
        raise Exception(f"Unexpected error reading documentation file for document: {doc_name}")

# --- Run Server ---
if __name__ == "__main__":
    logger.info(f"Serving documentation from: {DATA_DIR.resolve()}")
    logger.info(f"Using structure file: {STRUCTURE_FILE.resolve()}")
    logger.info(f"Resource URI prefix: {RESOURCE_PREFIX}")
    logger.info("Starting MCP server...")
    mcp.run(transport = "sse")
