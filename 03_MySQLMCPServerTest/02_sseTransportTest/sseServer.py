import uvicorn
import os
from fastapi import FastAPI, Request
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from mysqlMCPServer import mcp
from dotenv import load_dotenv


# 从环境变量获取主机地址，HOST默认为"0.0.0.0"（监听所有网络接口）,PORT默认为8000
load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


# 创建 FastAPI 应用实例，并设置元数据
app = FastAPI(
    title="FastAPI MCP SSE",
    description="一个展示服务器推送事件（SSE）与模型上下文协议（MCP）集成的用例",
    version="0.1.0",
)


# 创建 SSE 传输实例，用于处理服务器推送事件（Server-Sent Events）
# 指定 SSE 消息的路径为 "/messages/"
sse = SseServerTransport("/messages/")


# 将 /messages 路径挂载到 SSE 消息处理程序
# 用于处理客户端发送的消息
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))


# 定义 SSE 端点，处理与 MCP 服务器的连接
@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """
    连接到 MCP 服务器的 SSE 端点

    此端点与客户端建立服务器推送事件（SSE）连接，
    并将通信转发到模型上下文协议（MCP）服务器。
    """
    # 使用 sse.connect_sse 建立与 MCP 服务器的 SSE 连接
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        # 读取流，用于接收客户端消息
        read_stream,
        # 写入流，用于向客户端发送消息
        write_stream,
    ):
        # 运行 MCP 服务器，使用建立的读写流
        await mcp.run(
            # 传入读取流
            read_stream,
            # 传入写入流
            write_stream,
            # 创建 MCP 初始化选项
            mcp.create_initialization_options(),
        )


# 定义运行 FastAPI 服务器的函数
def run():
    """使用 uvicorn 启动 FastAPI 服务器"""
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


# 主程序入口
if __name__ == "__main__":
    # 运行 FastAPI 服务器
    run()
