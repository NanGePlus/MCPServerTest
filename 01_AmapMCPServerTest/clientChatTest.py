import asyncio
import json
import logging
import os
import shutil
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 用于管理MCP客户端的配置和环境变量
class Configuration:
    # 初始化对象，并加载环境变量
    def __init__(self) -> None:
        # 加载环境变量（通常从 .env 文件中读取）
        self.load_env()
        self.base_url = os.getenv("LLM_BASE_URL")
        self.api_key = os.getenv("LLM_API_KEY")
        self.chat_model = os.getenv("LLM_CHAT_MODEL")

    # @staticmethod，表示该方法不依赖于实例本身，可以直接通过类名调用
    @staticmethod
    def load_env() -> None:
        load_dotenv()

    # 从指定的 JSON 配置文件中加载配置
    # file_path: 配置文件的路径
    # 返回值: 一个包含配置信息的字典
    # FileNotFoundError: 文件不存在时抛出
    # JSONDecodeError: 配置文件不是有效的 JSON 格式时抛出
    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        # 打开指定路径的文件，以只读模式读取
        # 使用 json.load 将文件内容解析为 Python 字典并返回
        with open(file_path, 'r') as f:
            return json.load(f)

    # @property，将方法转换为只读属性，调用时不需要括号
    # 提供获取 llm_api_key 的接口
    @property
    def llm_api_key(self) -> str:
        # 检查 self.api_key 是否存在
        if not self.api_key:
            # 如果不存在，抛出 ValueError 异常
            raise ValueError("LLM_API_KEY not found in environment variables")
        # 返回 self.api_key 的值
        return self.api_key

    # @property，将方法转换为只读属性，调用时不需要括号
    # 提供获取 llm_base_url 的接口
    @property
    def llm_base_url(self) -> str:
        # 检查 self.base_url 是否存在
        if not self.base_url:
            # 如果不存在，抛出 ValueError 异常
            raise ValueError("LLM_BASE_URL not found in environment variables")
        # 返回 self.base_url 的值
        return self.base_url

    # @property，将方法转换为只读属性，调用时不需要括号
    # 提供获取 llm_chat_model 的接口
    @property
    def llm_chat_model(self) -> str:
        # 检查 self.base_url 是否存在
        if not self.chat_model:
            # 如果不存在，抛出 ValueError 异常
            raise ValueError("LLM_CHAT_MODEL not found in environment variables")
        # 返回 self.base_url 的值
        return self.chat_model


# 处理 MCP 服务器初始化、工具发现和执行
class Server:
    # 构造函数，在类实例化时调用
    # name: 服务器的名称
    # config: 配置字典，包含服务器的参数
    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name: str = name
        self.config: Dict[str, Any] = config
        # 标准输入/输出的上下文对象，用于与服务器交互
        self.stdio_context: Optional[Any] = None
        # 服务器的会话，用于发送请求和接收响应
        self.session: Optional[ClientSession] = None
        # 异步锁，用于确保清理资源的过程是线程安全的
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        # 存储服务器的能力
        self.capabilities: Optional[Dict[str, Any]] = None

    # 初始化服务器连接
    async def initialize(self) -> None:
        # server_params: 创建服务器参数对象
        # command: 如果配置中命令是 npx，使用系统路径查找，否则直接使用配置值
        # args: 从配置中获取命令行参数
        # env: 合并系统环境变量和配置中的自定义环境变量
        server_params = StdioServerParameters(
            command=shutil.which("npx") if self.config['command'] == "npx" else self.config['command'],
            args=self.config['args'],
            env={**os.environ, **self.config['env']} if self.config.get('env') else None
        )
        try:
            # 使用 stdio_client 初始化标准输入/输出上下文
            self.stdio_context = stdio_client(server_params)
            read, write = await self.stdio_context.__aenter__()
            # 创建 ClientSession 会话，并调用其 initialize 方法以获取服务器能力
            self.session = ClientSession(read, write)
            await self.session.__aenter__()
            self.capabilities = await self.session.initialize()
        # 发生异常时记录错误日志，调用 cleanup 清理资源并重新抛出异常
        except Exception as e:
            logging.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    # 从服务器获取可用工具列表
    async def list_tools(self) -> List[Any]:
        # 如果 session 未初始化，抛出运行时异常
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")
        # 调用会话的 list_tools 方法获取工具响应
        tools_response = await self.session.list_tools()
        # 初始化空列表 tools
        tools = []

        # 遍历工具响应，解析并存储工具信息
        for item in tools_response:
            if isinstance(item, tuple) and item[0] == 'tools':
                for tool in item[1]:
                    tools.append(Tool(tool.name, tool.description, tool.inputSchema))

        return tools

    # 执行指定工具，支持重试机制
    # tool_name: 工具名称
    # arguments: 执行工具所需的参数
    # retries: 最大重试次数
    # delay: 每次重试的间隔时间
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any], retries: int = 2,
                           delay: float = 1.0) -> Any:
        # 检查会话是否已初始化
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        # 循环尝试执行工具
        # 如果成功，返回执行结果
        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Executing {tool_name}...")
                result = await self.session.call_tool(tool_name, arguments)
                return result

            # 捕获异常时记录日志
            # 如果未超出最大重试次数，延迟后重试
            # 达到最大重试次数时抛出异常
            except Exception as e:
                attempt += 1
                logging.warning(f"Error executing tool: {e}. Attempt {attempt} of {retries}.")
                if attempt < retries:
                    logging.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logging.error("Max retries reached. Failing.")
                    raise

    # 从服务器获取可用资源列表
    async def list_resources(self) -> List[Any]:
        # 如果 session 未初始化，抛出运行时异常
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")
        # 调用会话的 list_resources 方法获取资源响应
        resources_response = await self.session.list_resources()
        # 初始化空列表 resources
        resources = []

        # 遍历资源响应，解析并存储资源信息
        for item in resources_response:
            if isinstance(item, tuple) and item[0] == 'resources':
                for resource in item[1]:
                    resources.append(
                        Resource(str(resource.uri), resource.name, resource.description, resource.mimeType))

        return resources

    # 读取指定资源，支持重试机制
    # resource_uri: 资源URI标识
    # retries: 最大重试次数
    # delay: 每次重试的间隔时间
    async def read_resource(self, resource_uri: str, retries: int = 2, delay: float = 1.0) -> Any:
        # 检查会话是否已初始化
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        # 循环尝试执行工具
        # 如果成功，返回执行结果
        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Executing {resource_uri}...")
                result = await self.session.read_resource(resource_uri)

                return result

            # 捕获异常时记录日志
            # 如果未超出最大重试次数，延迟后重试
            # 达到最大重试次数时抛出异常
            except Exception as e:
                attempt += 1
                logging.warning(f"Error executing resource: {e}. Attempt {attempt} of {retries}.")
                if attempt < retries:
                    logging.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logging.error("Max retries reached. Failing.")
                    raise

    # 清理服务器资源，确保资源释放
    async def cleanup(self) -> None:
        # 使用异步锁确保清理操作的线程安全
        # 清理会话资源，记录可能的警告
        async with self._cleanup_lock:
            try:
                if self.session:
                    try:
                        await self.session.__aexit__(None, None, None)
                    except Exception as e:
                        logging.warning(f"Warning during session cleanup for {self.name}: {e}")
                    finally:
                        self.session = None

                # 清理标准输入/输出上下文资源，捕获并记录不同类型的异常
                if self.stdio_context:
                    try:
                        await self.stdio_context.__aexit__(None, None, None)
                    except (RuntimeError, asyncio.CancelledError) as e:
                        logging.info(f"Note: Normal shutdown message for {self.name}: {e}")
                    except Exception as e:
                        logging.warning(f"Warning during stdio cleanup for {self.name}: {e}")
                    finally:
                        self.stdio_context = None
            # 捕获清理过程中可能的异常并记录错误日志
            except Exception as e:
                logging.error(f"Error during cleanup of server {self.name}: {e}")


# 代表各个资源及其属性和格式
class Resource:
    # 构造函数，在类实例化时调用
    # uri: 表的唯一资源标识符
    # name: 资源的名称
    # mimeType: MIME 类型，表示资源的数据类型
    # description: 描述信息
    def __init__(self, uri: str, name: str, description: str, mimeType: str) -> None:
        self.uri: str = uri
        self.name: str = name
        self.description: str = description
        self.mimeType: str = mimeType

    # 将资源的信息格式化为一个字符串，适合语言模型（LLM）使用
    def format_for_llm(self) -> str:
        return f"""
                URI: {self.uri}
                Name: {self.name}
                Description: {self.description}
                MimeType: {self.mimeType}
                """


# 代表各个工具及其属性和格式
class Tool:
    # 构造函数，在类实例化时调用
    # name: 工具的名称
    # description: 工具的描述信息
    # input_schema: 工具的输入架构，通常是一个描述输入参数的字典
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]) -> None:
        self.name: str = name
        self.description: str = description
        self.input_schema: Dict[str, Any] = input_schema

    # 将工具的信息格式化为一个字符串，适合语言模型（LLM）使用
    # 返回值: 包含工具名称、描述和参数信息的格式化字符串
    def format_for_llm(self) -> str:
        args_desc = []
        if 'properties' in self.input_schema:
            for param_name, param_info in self.input_schema['properties'].items():
                arg_desc = f"- {param_name}: {param_info.get('description', 'No description')}"
                if param_name in self.input_schema.get('required', []):
                    arg_desc += " (required)"
                args_desc.append(arg_desc)

        return f"""
                Tool: {self.name}
                Description: {self.description}
                Arguments:
                {chr(10).join(args_desc)}
                """


# 管理与LLM的通信
class LLMClient:
    def __init__(self, base_url: str, api_key: str, chat_model: str) -> None:
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.chat_model: str = chat_model

    # 向 LLM 发送请求，并返回其响应
    # messages: 一个字典列表，每个字典包含消息内容，通常是聊天对话的一部分
    # 返回值: 返回 LLM 的响应内容，类型为字符串
    # 如果请求失败，抛出 RequestException
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        # 指定 LLM 提供者的 API 端点，用于发送聊天请求
        url = self.base_url

        # Content-Type: 表示请求体的格式为 JSON
        # Authorization: 使用 Bearer 令牌进行身份验证，令牌为 self.api_key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 请求体数据，以字典形式表示
        # "messages": 包含传入的消息列表
        # "model": 使用的模型名称（例如 llama-3.2-90b-vision-preview）
        # "temperature": 控制生成的文本的随机性，0.7 表示适度随机
        # "max_tokens": 最大的输出 token 数量（4096），限制响应的长度
        # "top_p": 控制响应中最可能的 token 的累积概率，1 表示使用所有候选词
        payload = {
            "messages": messages,
            "temperature": 1.0,
            "top_p": 1.0,
            "max_tokens": 4000,
            "model": self.chat_model
        }

        try:
            # 使用 requests.post 发送 POST 请求，传递 URL、请求头和负载
            # url: 请求的 API 端点
            # headers: 请求头，包含 Content-Type 和 Authorizatio
            # json=payload: 将 payload 作为 JSON 格式传递
            response = requests.post(url, headers=headers, json=payload)
            # 如果响应的状态码表示错误（例如 4xx 或 5xx），则抛出异常
            response.raise_for_status()
            # 解析响应为 JSON 格式的数据
            data = response.json()
            # 从 JSON 响应中提取工具的输出内容
            return data['choices'][0]['message']['content']

        # 如果请求失败（如连接错误、超时或无效响应等），捕获 RequestException 异常
        # 记录错误信息，str(e) 提供异常的具体描述
        except requests.exceptions.RequestException as e:
            error_message = f"Error getting LLM response: {str(e)}"
            logging.error(error_message)
            # 如果异常中包含响应对象（e.response），进一步记录响应的状态码和响应内容
            # 这有助于分析请求失败的原因（例如服务端错误、API 限制等）
            if e.response is not None:
                status_code = e.response.status_code
                logging.error(f"Status code: {status_code}")
                logging.error(f"Response details: {e.response.text}")
            # 返回一个友好的错误消息给调用者，告知发生了错误并建议重试或重新措辞请求
            return f"I encountered an error: {error_message}. Please try again or rephrase your request."


# 协调用户、 LLM和工具之间的交互
class ChatSession:
    # servers: 一个 Server 类的列表，表示多个服务器的实例
    # llm_client: LLMClient 的实例，用于与 LLM 进行通信
    def __init__(self, servers: List[Server], llm_client: LLMClient) -> None:
        self.servers: List[Server] = servers
        self.llm_client: LLMClient = llm_client

    # 清理所有服务器
    # 创建清理任务: 遍历所有的服务器实例，为每个服务器创建一个清理任务（调用 server.cleanup()）
    # 并行执行清理任务: 使用 asyncio.gather 并发执行所有清理任务
    # return_exceptions=True 表示即使部分任务抛出异常，也会继续执行其它任务
    # 异常处理: 如果有异常，记录警告日志
    async def cleanup_servers(self) -> None:
        cleanup_tasks = []
        for server in self.servers:
            cleanup_tasks.append(asyncio.create_task(server.cleanup()))

        if cleanup_tasks:
            try:
                await asyncio.gather(*cleanup_tasks, return_exceptions=True)
            except Exception as e:
                logging.warning(f"Warning during final cleanup: {e}")

    # 负责处理从 LLM 返回的响应，并在需要时执行工具
    async def process_llm_response(self, llm_response: str) -> str:
        try:
            # 尝试将 LLM 响应解析为 JSON ，以便检查是否包含 tool 和 arguments 字段
            llm_call = json.loads(llm_response)

            # 1、如果响应包含工具名称和参数，执行相应工具
            if "tool" in llm_call and "arguments" in llm_call:
                logging.info(f"Executing tool: {llm_call['tool']}")
                logging.info(f"With arguments: {llm_call['arguments']}")
                # 遍历每个服务器，检查是否有与响应中的工具名称匹配的工具
                for server in self.servers:
                    try:
                        tools = await server.list_tools()
                        # 如果找到相应的工具
                        if any(tool.name == llm_call["tool"] for tool in tools):
                            try:
                                # 调用 server.execute_tool 来执行该工具
                                result = await server.execute_tool(llm_call["tool"], llm_call["arguments"])
                                # 返回工具的执行结果
                                return f"Tool execution result: {result}"
                            # 如果无法找到指定的工具或遇到错误，返回相应的错误信息
                            except Exception as e:
                                error_msg = f"Error executing tool: {str(e)}"
                                logging.error(error_msg)
                                return error_msg
                    except Exception as e:
                        logging.error(f"Server {server.name} does not have 'list_tools' method: {e}")
                        continue
                return f"No server found with tool: {llm_call['tool']}"

            # 2、如果响应包含资源名称和URI，执行读取相应的资源
            if "resource" in llm_call:
                logging.info(f"Executing resource: {llm_call['resource']}")
                logging.info(f"With URI: {llm_call['uri']}")
                # 遍历每个服务器，检查是否有与响应中的资源名称匹配的资源
                for server in self.servers:
                    try:
                        resources = await server.list_resources()
                        # 如果找到相应的资源
                        if any(resource.uri == llm_call["uri"] for resource in resources):
                            try:
                                # 调用 server.read_resource 来读取该资源
                                result = await server.read_resource(llm_call["uri"])
                                # 返回资源的执行结果
                                return f"Resource execution result: {result}"
                            # 如果无法找到指定的资源或遇到错误，返回相应的错误信息
                            except Exception as e:
                                error_msg = f"Error executing resource: {str(e)}"
                                logging.error(error_msg)
                                return error_msg
                    except Exception as e:
                        logging.error(f"Server {server.name} does not have 'list_resources' method: {e}")
                        continue
                return f"No server found with resource: {llm_call['uri']}"
            return llm_response

        # 如果响应无法解析为 JSON，返回原始 LLM 响应
        except json.JSONDecodeError:
            return llm_response

    # 方法: start 用于启动整个聊天会话，初始化服务器并开始与用户的互动
    async def start(self) -> None:
        try:
            # 初始化所有服务器: 遍历 self.servers，异步调用每个服务器的 initialize 方法
            for server in self.servers:
                try:
                    await server.initialize()
                # 异常处理: 如果服务器初始化失败，记录错误并调用 cleanup_servers 清理资源，然后退出会话
                except Exception as e:
                    logging.error(f"Failed to initialize server: {e}")
                    await self.cleanup_servers()
                    return

            # 遍历所有服务器，调用 list_tools() 获取每个服务器的工具列表
            all_tools = []
            for server in self.servers:
                try:
                    tools = await server.list_tools()
                    all_tools.extend(tools)
                except Exception as e:
                    print(f"Server {server.name} does not have 'list_tools' method: {e}")
            # 将所有工具的描述信息汇总，生成供 LLM 使用的工具描述字符串
            try:
                tools_description = "\n".join([tool.format_for_llm() for tool in all_tools])
            except Exception as e:
                print(f"Error while formatting resources for LLM: {e}")
                tools_description = ""

            # # 遍历所有服务器，调用 list_resources() 获取每个服务器的资源列表
            all_resources = []
            for server in self.servers:
                try:
                    resources = await server.list_resources()
                    all_resources.extend(resources)
                except Exception as e:
                    print(f"Server {server.name} does not have 'list_resources' method: {e}")
            # 将所有资源的描述信息汇总，生成供 LLM 使用的资源描述字符串
            try:
                resources_description = "\n".join([resource.format_for_llm() for resource in all_resources])
            except Exception as e:
                print(f"Error while formatting resources for LLM: {e}")
                resources_description = ""

            # 构建一个系统消息，作为 LLM 交互的指令，告知 LLM 使用哪些工具以及如何与用户进行交互
            # 系统消息强调 LLM 必须以严格的 JSON 格式请求工具，并且在工具响应后将其转换为自然语言响应
            system_message = f"""You are a helpful assistant with access to these resources and tools: 

                            resources:{resources_description}
                            tools:{tools_description}
                            Choose the appropriate resource or tool based on the user's question. If no resource or tool is needed, reply directly.

                            IMPORTANT: When you need to use a resource, you must ONLY respond with the exact JSON object format below, nothing else:
                            {{
                                "resource": "resource-name",
                                "uri": "resource-URI"
                            }}

                            After receiving a resource's response:
                            1. Transform the raw data into a natural, conversational response
                            2. Keep responses concise but informative
                            3. Focus on the most relevant information
                            4. Use appropriate context from the user's question
                            5. Avoid simply repeating the raw data

                            IMPORTANT: When you need to use a tool, you must ONLY respond with the exact JSON object format below, nothing else:
                            {{
                                "tool": "tool-name",
                                "arguments": {{
                                    "argument-name": "value"
                                }}
                            }}

                            After receiving a tool's response:
                            1. Transform the raw data into a natural, conversational response
                            2. Keep responses concise but informative
                            3. Focus on the most relevant information
                            4. Use appropriate context from the user's question
                            5. Avoid simply repeating the raw data

                            Please use only the resources or tools that are explicitly defined above."""

            # 消息初始化 创建一个消息列表，其中包含一个系统消息，指示 LLM 如何与用户交互
            messages = [
                {
                    "role": "system",
                    "content": system_message
                }
            ]

            # 交互循环
            while True:
                try:
                    # 等待用户输入，如果用户输入 quit 或 exit，则退出
                    user_input = input("user: ").strip().lower()
                    if user_input in ['quit', 'exit']:
                        logging.info("\nExiting...")
                        break

                    # 将用户输入添加到消息列表
                    messages.append({"role": "user", "content": user_input})

                    # 调用 LLM 客户端获取 LLM 的响应
                    llm_response = self.llm_client.get_response(messages)
                    logging.info("\nAssistant: %s", llm_response)

                    # 调用 process_llm_response 方法处理 LLM 响应，执行工具（如果需要）
                    result = await self.process_llm_response(llm_response)

                    # 如果工具执行结果与 LLM 响应不同，更新消息列表并再次与 LLM 交互，获取最终响应
                    if result != llm_response:
                        messages.append({"role": "assistant", "content": llm_response})
                        messages.append({"role": "system", "content": result})

                        final_response = self.llm_client.get_response(messages)
                        logging.info("\nFinal response: %s", final_response)
                        messages.append({"role": "assistant", "content": final_response})
                    else:
                        messages.append({"role": "assistant", "content": llm_response})

                # 处理 KeyboardInterrupt，允许用户中断会话
                except KeyboardInterrupt:
                    logging.info("\nExiting...")
                    break
        # 清理资源: 无论会话如何结束（正常结束或由于异常退出），都确保调用 cleanup_servers 清理服务器资源
        finally:
            await self.cleanup_servers()


async def main() -> None:
    # 创建一个 Configuration 类的实例
    config = Configuration()
    # 调用 Configuration 类中的 load_config 方法来加载配置文件 servers_config.json
    server_config = config.load_config('servers_config.json')
    # 遍历 server_config['mcpServers'] 字典，并为每个服务器创建一个 Server 实例，传入服务器名称 (name) 和配置信息 (srv_config)
    # 结果是一个 Server 对象的列表，保存在 servers 变量中
    servers = [Server(name, srv_config) for name, srv_config in server_config['mcpServers'].items()]
    # 创建一个 LLMClient 实例，用于与 LLM (大语言模型) 进行交互
    llm_client = LLMClient(config.llm_base_url, config.llm_api_key, config.llm_chat_model)
    # 创建一个 ChatSession 实例，负责管理与用户的聊天交互、LLM 响应和工具执行
    # 将之前创建的 servers 和 llm_client 传递给 ChatSession 构造函数，初始化会话
    chat_session = ChatSession(servers, llm_client)
    # 调用 ChatSession 类的 start 方法，启动聊天会话
    # 由于 start 是一个异步方法，所以使用 await 等待该方法执行完毕
    # start 方法将处理用户的输入、与 LLM 交互、执行工具（如果需要）等，并持续运行直到用户选择退出
    await chat_session.start()


if __name__ == "__main__":
    asyncio.run(main())

