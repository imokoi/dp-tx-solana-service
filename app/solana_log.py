import asyncio
import json
import websockets.typing as WebSocketTyping
from app.amm import pick_amm_v4_initialize2_log
import asyncio
import json
import websockets.legacy.client as WebSocketClient
import websockets.exceptions
from app.clmm import pick_clmm_create_pool_instruction_log
from app.common import SOLANA_MAIN_NET_WS_RPC
from app.solana_log import process_logs


async def subscribe_solana_logs():
    '''
    订阅solana的日志Log消息
    '''
    async with WebSocketClient.connect(SOLANA_MAIN_NET_WS_RPC) as websocket:
        # 构造订阅请求
        subscribe_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": ["all", {"commitment": "finalized"}]
        }

        # 发送订阅请求
        await websocket.send(json.dumps(subscribe_message))
        message = await websocket.recv()

        # 循环接收日志消息
        try:
            while True:
                message = await websocket.recv()
                await process_logs(message)
        except websockets.exceptions.ConnectionClosed:
            print("Connection with server closed")


async def process_logs(log_data: WebSocketTyping.Data):
    '''
    解析solana的日志Log消息
    '''
    message_dict = json.loads(log_data)
    try:
        logs = message_dict["params"]["result"]["value"]["logs"]
        signature = message_dict["params"]["result"]["value"]["signature"]
        errr = message_dict["params"]["result"]["value"]["err"]

        # 过滤失败的tx
        if errr:
            print(f"Error: {errr}")
            return

        # 提取 AMM v4 的创建提取池子的日志
        asyncio.create_task(pick_amm_v4_initialize2_log(signature, logs))

        # 提取 CLMM 的创建提取池子的日志
        asyncio.create_task(pick_clmm_create_pool_instruction_log(signature, logs))
    except Exception as e:
        print(f"Error: {e}")
