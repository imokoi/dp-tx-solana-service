import asyncio
import json

import websockets

SOLANA_MAIN_NET_HTTP_RPC = "https://api.mainnet-beta.solana.com"
SOLANA_MAIN_NET_WS_RPC = "wss://api.mainnet-beta.solana.com"

SOLANA_DEV_NET_HTTP_RPC = "https://api.devnet.solana.com"
SOLANA_DEV_NET_WS_RPC = "wss://api.devnet.solana.com"


async def connect_ws():
    async with websockets.connect(SOLANA_DEV_NET_WS_RPC) as websocket:
        # 构造订阅请求
        subscribe_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": ["all"]
        }

        # 发送订阅请求
        await websocket.send(json.dumps(subscribe_message))

        # 循环接收日志消息
        try:
            while True:
                message = await websocket.recv()
                print(f"Received log: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection with server closed")


if __name__ == "__main__":
    asyncio.run(connect_ws())
