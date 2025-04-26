# 1、项目介绍                  
## 1.1、主要内容                                     
如何使用高德地图MCP Server                      

## 1.2 MCP介绍                              
MCP(Model Context Protocol 模型上下文协议)是Claude开源的一种开放协议，可实现LLM应用程序与外部数据源和工具之间的无缝集成                                      
MCP官方简介:https://www.anthropic.com/news/model-context-protocol                                                                                   
MCP文档手册:https://modelcontextprotocol.io/introduction                                               
MCP官方服务器列表:https://github.com/modelcontextprotocol/servers                       
PythonSDK的github地址:https://github.com/modelcontextprotocol/python-sdk                    
关于MCP的详细介绍，参考这期视频如下:                    
https://www.bilibili.com/video/BV1HBquYbE7t/                                  
https://youtu.be/Jmo7rgb_OXQ                            

## 1.3 高德地图 MCP Server 
为实现 LBS 服务与 LLM 更好的交互，高德地图 MCP Server 现已覆盖12大核心服务接口，提供全场景覆盖的地图服务                
包括地理编码、逆地理编码、IP 定位、天气查询、骑行路径规划、步行路径规划、驾车路径规划、公交路径规划、距离测量、关键词搜索、周边搜索、详情搜索等                 
链接地址:https://lbs.amap.com/api/mcp-server/summary              
具体提供的接口详情介绍:                  
**(1)地理编码**                
name='maps_regeocode'               
description='将一个高德经纬度坐标转换为行政区划地址信息'                       
inputSchema={'type': 'object', 'properties': {'location': {'type': 'string', 'description': '经纬度'}}, 'required': ['location']}                   
**(2)逆地理编码**               
name='maps_geo'              
description='将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标'               
inputSchema={'type': 'object', 'properties': {'address': {'type': 'string', 'description': '待解析的结构化地址信息'}, 'city': {'type': 'string', 'description': '指定查询的城市'}}, 'required': ['address']}                  
**(3)IP 定位**               
name='maps_ip_location'         
description='IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置'            
inputSchema={'type': 'object', 'properties': {'ip': {'type': 'string', 'description': 'IP地址'}}, 'required': ['ip']}                
**(4)天气查询**               
name='maps_weather'               
description='根据城市名称或者标准adcode查询指定城市的天气'                 
inputSchema={'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名称或者adcode'}}, 'required': ['city']}             
**(5)骑行路径规划**               
name='maps_bicycling'     
description='骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划'     
inputSchema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']}      
**(6)步行路径规划**               
name='maps_direction_walking'      
description='步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据'       
inputSchema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经度，纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']}        
**(7)驾车路径规划**                
name='maps_direction_driving'          
description='驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据。'            
inputSchema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经度，纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']}            
**(8)公交路径规划**              
name='maps_direction_transit_integrated'           
description='公交路径规划 API 可以根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市'           
inputSchema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经度，纬度，坐标格式为：经度，纬度'}, 'city': {'type': 'string', 'description': '公共交通规划起点城市'}, 'cityd': {'type': 'string', 'description': '公共交通规划终点城市'}}, 'required': ['origin', 'destination', 'city', 'cityd']}         
**(9)距离测量**              
name='maps_distance'            
description='距离测量 API 可以测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量'      
inputSchema={'type': 'object', 'properties': {'origins': {'type': 'string', 'description': '起点经度，纬度，可以传多个坐标，使用分号隔离，比如120,30;120,31，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '终点经度，纬度，坐标格式为：经度，纬度'}, 'type': {'type': 'string', 'description': '距离测量类型,1代表驾车距离测量，0代表直线距离测量，3步行距离测量'}}, 'required': ['origins', 'destination']}        
**(10)关键词搜索**         
name='maps_text_search'           
description='关键词搜，根据用户传入关键词，搜索出相关的POI'           
inputSchema={'type': 'object', 'properties': {'keywords': {'type': 'string', 'description': '搜索关键词'}, 'city': {'type': 'string', 'description': '查询城市'}, 'types': {'type': 'string', 'description': 'POI类型，比如加油站'}}, 'required': ['keywords']}              
**(11)周边搜索**            
name='maps_search_detail'            
description='查询关键词搜或者周边搜获取到的POI ID的详细信息'              
inputSchema={'type': 'object', 'properties': {'id': {'type': 'string', 'description': '关键词搜或者周边搜获取到的POI ID'}}, 'required': ['id']}              
**(12)详情搜索**                 
name='maps_around_search'            
description='周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI'              
inputSchema={'type': 'object', 'properties': {'keywords': {'type': 'string', 'description': '搜索关键词'}, 'location': {'type': 'string', 'description': '中心点经度纬度'}, 'radius': {'type': 'string', 'description': '搜索半径'}}, 'required': ['location']})]               


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
pip install mcp==1.6.0                     
pip install requests==2.32.3                                                                          
**注意:** 截止2025.04.25mcp最新版本为1.6.0，建议先使用要求的对应版本进行本项目测试，避免因版本升级造成的代码不兼容。测试通过后，可进行升级测试                      
     

# 4、功能测试
## 4.1 MCP服务功能接口测试            
首先需要下载并安装node的环境，直接下载 https://nodejs.org/zh-cn 安装包进行安装即可                        
进入到01_AmapMCPServerTest/amapMCPServerTest.py运行脚本进行服务接口的单独验证测试              

## 4.2 MCP Client测试   
进入到01_AmapMCPServerTest/clientChatTest.py运行脚本进行服务接口的单独验证测试                             
在运行脚本之前，需要在.env文件中配置大模型相关的参数及在servers_config.json文件中配置需要使用的MCP Server               
获取经纬度工具:http://www.jsons.cn/lngcode/                    
测试问题参考所示:               
(1)这个118.79815,32.01112经纬度对应的地方是哪里                           
(2)夫子庙的经纬度坐标是多少                  
(3)112.10.22.229这个IP所在位置                   
(4)上海的天气如何              
(5)我要从苏州的虎丘区骑行到相城区，帮我规划下路径            
(6)我要从苏州的虎丘区步行到相城区，帮我规划下路径            
(7)我要从苏州的虎丘区驾车到相城区，帮我规划下路径              
(8)我要从苏州的虎丘区坐公共交通到相城区，帮我规划下               
(9)测量下从苏州的虎丘区到相城区驾车距离是多少               
(10)在苏州虎丘区中石化的加油站有哪些，需要有POI的ID               
(11)POI为B020016GPH的详细信息               
(12)在苏州乐园周围10公里的中石化的加油站                

