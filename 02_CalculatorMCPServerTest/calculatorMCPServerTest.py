# ClientSession 表示客户端会话，用于与服务器交互
# StdioServerParameters 定义与服务器的 stdio 连接参数
# stdio_client 提供与服务器的 stdio 连接上下文管理器
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio




# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是 python
    command="python",
    # 启动命令的附加参数，这里是运行 example_server.py
    args=["calculatorMCPServer.py"],
    # 环境变量，默认为 None，表示使用当前环境变量
    env=None
)


# 服务器端功能测试
async def run():
    # 创建与服务器的标准输入/输出连接，并返回 read 和 write 流
    async with stdio_client(server_params) as (read, write):
        # 创建一个客户端会话对象，通过 read 和 write 流与服务器交互
        async with ClientSession(read, write) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
            capabilities = await session.initialize()
            print(f"Supported capabilities:{capabilities.capabilities}/n/n")

            # 请求服务器列出所有支持的 tools
            tools = await session.list_tools()
            print(f"Supported tools:{tools}/n/n")

            with open("output.txt", 'w', encoding='utf-8') as file:
                file.write(str(tools))


            # 文件相关功能测试
            add_result = await session.call_tool("add", arguments={"a":6, "b":3})
            subtract_result = await session.call_tool("subtract", arguments={"a":6, "b":3})
            multiply_result = await session.call_tool("multiply", arguments={"a":6, "b":3})
            divide_result = await session.call_tool("divide", arguments={"a":6, "b":3})
            print(f"add_result:{add_result}/n/n")
            print(f"subtract_result:{subtract_result}/n/n")
            print(f"multiply_result:{multiply_result}/n/n")
            print(f"divide_result:{divide_result}/n/n")



if __name__ == "__main__":
    # 使用 asyncio 启动异步的 run() 函数
    asyncio.run(run())
