# ClientSession 表示客户端会话，用于与服务器交互
# StdioServerParameters 定义与服务器的 stdio 连接参数
# stdio_client 提供与服务器的 stdio 连接上下文管理器
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio





# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是 python
    command="npx",
    # 启动命令的附加参数，这里是运行 example_server.py
    args=["-y", "@amap/amap-maps-mcp-server"],
    # 环境变量，默认为 None，表示使用当前环境变量
    env={"AMAP_MAPS_API_KEY": "608530313a6cd49be46145h5d9cefa25"}
)


# 服务器端功能测试
async def run():
    # 创建与服务器的标准输入/输出连接，并返回 read 和 write 流
    async with stdio_client(server_params) as (read, write):
        # 创建一个客户端会话对象，通过 read 和 write 流与服务器交互
        async with ClientSession(read, write) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
            # capabilities = await session.initialize()
            # print(f"Supported capabilities:{capabilities.capabilities}/n/n")

            # 请求服务器列出所有支持的 tools
            tools = await session.list_tools()
            print(f"Supported tools:{tools}/n/n")

            with open("output.txt", 'w', encoding='utf-8') as file:
                file.write(str(tools))

            # 相关功能测试
            # 1、将一个高德经纬度坐标转换为行政区划地址信息 http://www.jsons.cn/lngcode/
            # maps_regeocode = await session.call_tool("maps_regeocode", arguments={"location":"118.79815,32.01112"})
            # print(f"maps_geo:{maps_regeocode}/n/n")
            # print(f"maps_geo:{maps_regeocode.content[0].text}/n/n")

            # 2、将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标
            # maps_geo = await session.call_tool("maps_geo", arguments={"address":"南京夫子庙"})
            # print(f"maps_geo:{maps_geo}/n/n")
            # print(f"maps_geo:{maps_geo.content[0].text}/n/n")

            # 3、IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置
            # maps_ip_location = await session.call_tool("maps_ip_location", arguments={"ip":"112.10.22.229"})
            # print(f"maps_ip_location:{maps_ip_location}/n/n")
            # print(f"maps_ip_location:{maps_ip_location.content[0].text}/n/n")

            # 4、根据城市名称或者标准adcode查询指定城市的天气
            # # maps_weather = await session.call_tool("maps_weather", arguments={"city":"上海"})
            # maps_weather = await session.call_tool("maps_weather", arguments={"city":"310000"})
            # print(f"maps_weather:{maps_weather}/n/n")
            # print(f"maps_weather:{maps_weather.content[0].text}/n/n")

            # 5、骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划
            # 苏州虎丘区到相城区
            # maps_bicycling = await session.call_tool("maps_bicycling", arguments={"origin":"120.57345,31.2953","destination":"120.64239,31.36889"})
            # print(f"maps_bicycling:{maps_bicycling}/n/n")
            # print(f"maps_bicycling:{maps_bicycling.content[0].text}/n/n")

            # 6、步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据
            # 苏州虎丘区到相城区
            # maps_direction_walking = await session.call_tool("maps_direction_walking", arguments={"origin":"120.57345,31.2953","destination":"120.64239,31.36889"})
            # print(f"maps_direction_walking:{maps_direction_walking}/n/n")
            # print(f"maps_direction_walking:{maps_direction_walking.content[0].text}/n/n")

            # 7、驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据
            # 苏州虎丘区到相城区
            # maps_direction_driving = await session.call_tool("maps_direction_driving", arguments={"origin":"120.57345,31.2953","destination":"120.64239,31.36889"})
            # print(f"maps_direction_driving:{maps_direction_driving}/n/n")
            # print(f"maps_direction_driving:{maps_direction_driving.content[0].text}/n/n")

            # 8、公交路径规划 API 可以根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市
            # 苏州虎丘区到相城区
            # maps_direction_transit_integrated = await session.call_tool("maps_direction_transit_integrated", arguments={"origin":"120.57345,31.2953","destination":"120.64239,31.36889","city":"苏州","cityd":"苏州"})
            # print(f"maps_direction_transit_integrated:{maps_direction_transit_integrated}/n/n")
            # print(f"maps_direction_transit_integrated:{maps_direction_transit_integrated.content[0].text}/n/n")

            # 9、距离测量 API 可以测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量
            # 苏州虎丘区到相城区
            # 距离测量类型,1代表驾车距离测量，0代表直线距离测量，3步行距离测量
            # maps_distance = await session.call_tool("maps_distance", arguments={"origins":"120.57345,31.2953","destination":"120.64239,31.36889","type":"1"})
            # print(f"maps_distance:{maps_distance}/n/n")
            # print(f"maps_distance:{maps_distance.content[0].text}/n/n")

            # # 10、关键词搜，根据用户传入关键词，搜索出相关的POI
            # maps_text_search = await session.call_tool("maps_text_search", arguments={"keywords":"虎丘区中石化","city":"苏州","types":"加油站"})
            # print(f"maps_text_search:{maps_text_search}/n/n")
            # print(f"maps_text_search:{maps_text_search.content[0].text}/n/n")

            # 11、查询关键词搜或者周边搜获取到的POI（Point of Interest，兴趣点 ID的详细信息
            # maps_search_detail = await session.call_tool("maps_search_detail", arguments={"id":"B02000JR8M"})
            # print(f"maps_search_detail:{maps_search_detail}/n/n")
            # print(f"maps_search_detail:{maps_search_detail.content[0].text}/n/n")

            # 12、周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI
            # maps_around_search = await session.call_tool("maps_around_search", arguments={"keywords":"中石化","location":"120.57345,31.2953","radius":"4000"})
            # print(f"maps_around_search:{maps_around_search}/n/n")
            # print(f"maps_around_search:{maps_around_search.content[0].text}/n/n")



if __name__ == "__main__":
    # 使用 asyncio 启动异步的 run() 函数
    asyncio.run(run())
