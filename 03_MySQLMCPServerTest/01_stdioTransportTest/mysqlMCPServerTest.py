# ClientSession 表示客户端会话，用于与服务器交互
# StdioServerParameters 定义与服务器的 stdio 连接参数
from mcp import ClientSession, StdioServerParameters
# 提供与服务器的 stdio 连接上下文管理器
from mcp.client.stdio import stdio_client
import asyncio



# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是 python
    command="python",
    # 启动命令的附加参数，这里是运行 example_server.py
    args=["mysqlMCPServer.py"],
    # 环境变量，默认为 None，表示使用当前环境变量
    env=None
)


async def run():
    # 创建与服务器的标准输入/输出连接，并返回 read_stream 和 write_stream 流
    async with stdio_client(server_params) as (read_stream, write_stream):
        # 创建一个客户端会话对象，通过 read_stream 和 write_stream 流与服务器交互
        async with ClientSession(read_stream, write_stream) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
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