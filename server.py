# e:/mcp_docs_server/server.py
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base

# 创建一个名为 "DocSearcher" 的 MCP 服务器实例
mcp = FastMCP("DocSearcher")

# --- 示例 Resource ---
@mcp.resource("example://hello")
def get_example_resource() -> str:
    """一个简单的示例 Resource"""
    print("Executing example resource")
    return "Hello from Resource!"

# --- 示例 Tool ---
@mcp.tool()
def example_tool(message: str, ctx: Context) -> str:
    """一个简单的示例 Tool"""
    print(f"Executing example tool with message: {message}")
    ctx.info("Example tool executed successfully.") # 使用 Context 发送日志信息
    return f"Tool processed: {message}"

# --- 示例 Prompt ---
@mcp.prompt()
def example_prompt(topic: str) -> list[base.Message]:
    """一个简单的示例 Prompt"""
    print(f"Generating example prompt for topic: {topic}")
    return [
        base.UserMessage(f"Tell me about {topic}."),
        base.AssistantMessage("Okay, I can tell you about that topic.")
    ]

# 如果直接运行此文件，则启动服务器
if __name__ == "__main__":
    mcp.run()
