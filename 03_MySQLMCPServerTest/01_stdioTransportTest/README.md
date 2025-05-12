# 1、项目介绍                  
## 1.1、主要内容
在MCP系列视频中为大家实现过一个四则运算的MCP Server，是使用的FastMCP来开发的MCP Server，FastMCP是在低层MCP SDK上封装的简易框架，隐藏了细节               
那本期视频会使用官方低层MCP SDK方式并使用**STDIO传输模式**实现一个与MySQL连接的MCP Server，实现数据源访问和工具使用(SQL语句执行增删改查及联表查询)            

## 1.2 MCP概念介绍              
MCP官方简介:https://www.anthropic.com/news/model-context-protocol                                                                                       
MCP文档手册:https://modelcontextprotocol.io/introduction                                                   
MCP官方服务器列表:https://github.com/modelcontextprotocol/servers                             
PythonSDK的github地址:https://github.com/modelcontextprotocol/python-sdk                       
大家在实操今天的用例之前，可以通过下面这期视频了解下MCP相关内容，有关于STDIO传输模式的介绍                          
【大模型应用开发-MCP系列】03 为什么会出现MCP？MCP新标准(03.26版)3种传输模式,STDIO、HTTP+SSE、Streamable HTTP                     
https://youtu.be/EId3Kbmb_Ao           
https://www.bilibili.com/video/BV1ZHEgzXEP1/                 

## 1.3 自定义 MySQL MCP Server 
实现一个与MySQL连接的MCP Server，实现数据源访问和工具使用(SQL语句执行增删改查及联表查询)，具体提供的接口详情介绍:                                            
**(1)获取资源 URI**                           
uri=AnyUrl('mysql://students/data')                            
**(2)SQL语句执行**                         
name='execute_sql'                    
description='Execute an SQL query on the MySQL server'                     
inputSchema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'The SQL query to execute'}}, 'required': ['query']}, annotations=None               


# 2、前期准备工作
## 2.1 集成开发环境搭建  
anaconda提供python虚拟环境,pycharm提供集成开发环境                                              
**具体参考如下视频:**                        
【大模型应用开发-入门系列】03 集成开发环境搭建-开发前准备工作                         
https://youtu.be/KyfGduq5d7w                     
https://www.bilibili.com/video/BV1nvdpYCE33/                      

## 2.2 大模型LLM服务接口调用方案
(1)gpt大模型等国外大模型使用方案                  
国内无法直接访问，可以使用代理的方式，具体代理方案自己选择                        
这里推荐大家使用:https://nangeai.top/register?aff=Vxlp                        
(2)非gpt大模型方案 OneAPI方式或大模型厂商原生接口                                              
(3)本地开源大模型方案(Ollama方式)                                              
**具体参考如下视频:**                                           
【大模型应用开发-入门系列】04 大模型LLM服务接口调用方案                    
https://youtu.be/mTrgVllUl7Y               
https://www.bilibili.com/video/BV1BvduYKE75/                             


# 3、项目初始化
## 3.1 下载源码
GitHub或Gitee中下载工程文件到本地，下载地址如下：                
https://github.com/NanGePlus/MCPServerTest                                                                    
https://gitee.com/NanGePlus/MCPServerTest                                                              

## 3.2 构建项目 
使用pycharm构建一个项目，为项目配置虚拟python环境                         
项目名称：MCPServerTest                                          
虚拟环境名称保持与项目名称一致                            

## 3.3 将相关代码拷贝到项目工程中           
将下载的代码文件夹中的文件全部拷贝到新建的项目根目录下                             

## 3.4 安装项目依赖                            
新建命令行终端，在终端中运行如下指令进行安装         
pip install --upgrade mcp==1.8.0                                                  
pip install requests==2.32.3                          
pip install mysql-connector-python==9.3.0              
**注意:** 截止2025.05.12 mcp最新版本为1.8.0，建议先使用要求的对应版本进行本项目测试，避免因版本升级造成的代码不兼容。测试通过后，可进行升级测试                         
     

# 4、功能测试
## 4.1 启动Docker服务            
首先需要下载并安装docker，直接官网下载 https://www.docker.com/ 安装包进行安装即可                         
打开命令行终端，进入到supportFiles/docker-compose.yaml文件所在的目录，运行如下指令                    
docker-compose up -d                
启动成功后，通过数据库客户端软件连接到本地数据库，并将students_info.sql和students_score.sql文件导入到数据库中作为测试数据表                    

## 4.2 MCP Client测试   
首先，进入到03_MySQLMCPServerTest/01_stdioTransportTest中运行脚本mysqlMCPServerTest.py进行服务接口的单独验证测试                                       
最后，进入到03_MySQLMCPServerTest/01_stdioTransportTest中运行脚本clientChatTest.py使用大模型进行测试，在运行脚本之前，需要在.env文件中配置大模型相关的参数及在servers_config.json文件中配置需要使用的MCP Server              
测试问题，可参考如下:                                
(1)有哪些表可以使用                                             
(2)查询学生信息表中数据                                                   
(3)查询学生成绩表中数据                                               
(4)查询学生成绩表中分数最高的                                              
(5)对学生信息表和学生成绩表进行联表查询，生成每个学生姓名、成绩                     
(6)将学生姓名为张三的改为钱八，并获取最新的信息表       

         
 