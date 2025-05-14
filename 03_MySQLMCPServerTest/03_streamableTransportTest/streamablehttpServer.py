import uvicorn
import os
from mysqlMCPServer import mcp
from dotenv import load_dotenv
import contextlib
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send
import logging
from collections.abc import AsyncIterator



# 创建日志记录器，命名为当前模块名
logger = logging.getLogger(__name__)

# 从环境变量获取主机地址，HOST默认为"0.0.0.0"（监听所有网络接口）,PORT默认为8000
load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


# 创建流式HTTP会话管理器，启用真正的无状态模式
session_manager = StreamableHTTPSessionManager(
    # 传入mcp应用程序实例
    app=mcp,
    # 事件存储设置为None
    event_store=None,
    # JSON响应设置为None
    json_response=None,
    # 启用无状态模式
    stateless=True,
)


# 定义异步函数，用于处理流式HTTP请求
async def handle_streamable_http(
    # 请求的作用域
    scope: Scope,
    # 接收请求的函数
    receive: Receive,
    # 发送响应的函数
    send: Send
) -> None:
    # 调用会话管理器处理请求
    await session_manager.handle_request(scope, receive, send)


# 定义异步上下文管理器，用于管理应用程序生命周期
@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    """上下文管理器，用于管理会话管理器的生命周期"""
    # 启动会话管理器
    async with session_manager.run():
        # 记录应用程序启动日志
        logger.info("Application started with StreamableHTTP session manager!")
        try:
            # 进入生命周期，允许应用程序运行
            yield
        finally:
            # 记录应用程序关闭日志
            logger.info("Application shutting down...")


# 创建Starlette ASGI应用程序
starlette_app = Starlette(
    # 启用调试模式
    debug=True,
    routes=[
        # 挂载/mcp路由，关联处理流式HTTP请求的函数
        Mount("/mcp", app=handle_streamable_http),
    ],
    # 设置生命周期管理器
    lifespan=lifespan,
)


# 定义运行服务器的函数
def run():
    # 使用uvicorn运行Starlette应用程序
    uvicorn.run(starlette_app, host=HOST, port=PORT, log_level="info")



# 主程序入口
if __name__ == "__main__":
    # 运行服务器
    run()