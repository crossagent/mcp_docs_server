# e:/mcp_docs_server/server.py
import json
import os
import logging
import urllib.parse  # 添加这个导入
import asyncio  # 新增导入
from pathlib import Path
from typing import Any, Dict, List, Union, Optional

from mcp import Resource
from mcp.server.fastmcp import Context, FastMCP
from scripts import scrape_content # 新增导入

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
mcp = FastMCP("MCPDocsAssistant", port = 8020)

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

# --- Tool to Trigger Documentation Update ---
@mcp.tool(
    annotations={
        "title": "更新文档内容",
        "readOnlyHint": False,  # It modifies local files
        "destructiveHint": False, # Overwrites, but not typically 'destructive' user data loss
        "idempotentHint": False, # Running again fetches latest, so not idempotent
        "openWorldHint": True   # Interacts with external website
    }
)
async def trigger_doc_update() -> str:
    """
    触发后台任务以从官网抓取并更新本地文档内容。
    此操作会覆盖 data/ 目录下的现有 Markdown 文件和 structure_with_summaries.json。
    """
    logger.info("Received request to trigger documentation update.")
    try:
        # 使用 asyncio.create_task 在后台运行抓取脚本
        # 注意：FastMCP 可能已经在事件循环中运行，直接调用 main 可能阻塞
        # 更健壮的方法是使用 run_in_executor 或确保 scrape_content 是异步兼容的
        # 这里为了简单起见，我们先尝试直接调用，但标记为潜在的阻塞点
        # TODO: Consider running scrape_content.main in an executor to avoid blocking the event loop
        logger.info("Starting documentation scraping task in the background...")
        # 直接调用 main 函数，因为它本身不是 async def
        # 如果 scrape_content.main() 耗时很长，这仍然会阻塞当前事件循环
        # 正确的做法是将 scrape_content.main() 包装或重构为异步，或者使用 run_in_executor

        # 简单的后台任务启动（可能仍阻塞，取决于 scrape_content 实现）
        async def run_scrape():
            try:
                logger.info("Background scraping task started.")
                scrape_content.main() # 调用同步函数
                logger.info("Background scraping task finished successfully.")
                # 可选：在这里添加通知机制，告知更新完成
            except Exception as e:
                logger.error(f"Background scraping task failed: {str(e)}", exc_info=True)

        asyncio.create_task(run_scrape()) # 启动后台任务

        return "文档内容更新任务已启动。请稍后检查日志或文件系统确认完成。"
    except Exception as e:
        error_msg = f"启动文档更新任务时出错: {str(e)}"
        logger.error(error_msg, exc_info=True)
        # 根据 MCP 文档，工具错误应该在返回结果中体现，而不是抛出协议错误
        # 但 FastMCP 的 @mcp.tool 装饰器似乎直接处理函数返回值作为结果
        # 如果需要返回错误结构，可能需要调整 FastMCP 或返回特定格式的字符串/JSON
        return f"错误: {error_msg}" # 返回错误信息给客户端

# --- Run Server ---
if __name__ == "__main__":
    logger.info(f"Serving documentation from: {DATA_DIR.resolve()}")
    logger.info(f"Using structure file: {STRUCTURE_FILE.resolve()}")
    logger.info(f"Resource URI prefix: {RESOURCE_PREFIX}")
    logger.info("Starting MCP server...")
    mcp.run(transport = "sse")
