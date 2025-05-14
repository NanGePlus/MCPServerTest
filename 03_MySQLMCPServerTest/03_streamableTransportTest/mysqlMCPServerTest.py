from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio


async def run():
    # 创建与服务器的SSE连接，并返回 read_stream 和 write_stream 流
    async with streamablehttp_client(url="http://127.0.0.1:8000/mcp") as (read_stream, write_stream, get_session_id_callback):
        # # 创建一个客户端会话对象，通过 read_stream 和 write_stream 流与服务器交互
        async with ClientSession(read_stream, write_stream) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
            # Initialize the connection
            capabilities = await session.initialize()
            print(f"Supported capabilities:{capabilities.capabilities}/n/n")

            # 请求服务器列出所有支持的资源
            resources = await session.list_resources()
            print(f"Supported resources:{resources}/n/n")

            # 获取某具体资源 即某张表中的内容
            resources = await session.read_resource('mysql://students_info/data')
            print(f"Supported resources:",resources)
            # with open("output.txt", 'w', encoding='utf-8') as file:
            #     file.write(str(resources))

            # 获取可用的工具列表
            tools = await session.list_tools()
            print(f"Supported tools:{tools}/n/n")
            # with open("output.txt", 'w', encoding='utf-8') as file:
            #     file.write(str(tools))

            # 工具功能测试
            # result = await session.call_tool("execute_sql",{"query":"SHOW TABLES"})
            result = await session.call_tool("execute_sql",{"query":"SELECT * FROM students_info"})
            print(f"Supported result:{result}")


if __name__ == "__main__":
    # 使用 asyncio 启动异步的 run() 函数
    asyncio.run(run())