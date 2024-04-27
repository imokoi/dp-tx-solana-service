import asyncio
import json

import websockets.legacy.client as WebSocketClient
import websockets.exceptions

from app.common import SOLANA_MAIN_NET_WS_RPC
from app.transaction import process_logs


async def connect_ws_rpc():
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


if __name__ == "__main__":
    asyncio.run(connect_ws_rpc())
    # asyncio.run(get_transaction("5WXz8C15zkXsLtihXaAYHUyg7UtuFYZDVu7CzS8aWq1k3BREphkxBKTSDc3ZQ7GxgUMKQQbPQhUtiTC9DTM2cPVM"))
