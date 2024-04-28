import asyncio
import websockets
import websockets.legacy.server as WebSocketServer
import websockets.exceptions

# 存储所有已连接的WebSocket客户端
connected_clients = set()


async def start_websocket_server():
    # 启动服务器
    async with WebSocketServer.serve(handler, "0.0.0.0", 8081):
        print("Websocket server started")
        await asyncio.Future()  # 运行服务器直到被手动停止


async def handler(websocket, path):
    # 添加新客户端到集合中
    connected_clients.add(websocket)
    try:
        # 这里可以根据需要处理进来的消息
        async for message in websocket:
            print(f"Received message: {message}")
            # 回应消息
            await websocket.send("Message received")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    finally:
        # 客户端断开连接后，从集合中移除
        connected_clients.remove(websocket)


async def broadcast_message(message):
    '''
    广播消息给所有连接的客户端
    '''
    if connected_clients:  # 检查是否有连接的客户端
        await asyncio.wait([client.send(message) for client in connected_clients])


# 例如，你可以在特定的时间点调用这个函数
# async def schedule_broadcast():
#     await asyncio.sleep(10)  # 假设延迟10秒后发送
#     await broadcast_message("Hello, everyone!")
