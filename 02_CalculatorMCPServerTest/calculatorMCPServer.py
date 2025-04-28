import logging
from asyncio import timeout

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# 日志相关配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("calculator_mcp_server")

# 初始化 FastMCP 服务器，指定服务名称为 "calculator"
mcp = FastMCP("calculator")

# 定义加法工具函数
@mcp.tool()
async def add(a: float, b: float) -> list[TextContent]:
    """执行加法运算

    Args:
        a: 第一个数字
        b: 第二个数字
    """
    logger.info(f"Add operation: {a} + {b}")
    result = a + b
    return [TextContent(type="text", text=str(result))]

# 定义减法工具函数
@mcp.tool()
async def subtract(a: float, b: float) -> list[TextContent]:
    """执行减法运算

    Args:
        a: 第一个数字
        b: 第二个数字
    """
    logger.info(f"Subtract operation: {a} - {b}")
    result = a - b
    return [TextContent(type="text", text=str(result))]

# 定义乘法工具函数
@mcp.tool()
async def multiply(a: float, b: float) -> list[TextContent]:
    """执行乘法运算

    Args:
        a: 第一个数字
        b: 第二个数字
    """
    logger.info(f"Multiply operation: {a} * {b}")
    result = a * b
    return [TextContent(type="text", text=str(result))]

# 定义除法工具函数
@mcp.tool()
async def divide(a: float, b: float) -> list[TextContent]:
    """执行除法运算

    Args:
        a: 第一个数字
        b: 第二个数字
    """
    logger.info(f"Divide operation: {a} / {b}")
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    result = a / b
    return [TextContent(type="text", text=str(result))]

# 主程序入口
if __name__ == "__main__":
    # 初始化并运行 FastMCP 服务器，使用标准输入输出作为传输方式
    mcp.run(transport='stdio')