import asyncio
import json

import websockets.legacy.client as WebSocketClient
import websockets.exceptions

from app.clmm import parse_clmm_transaction
from app.common import SOLANA_MAIN_NET_WS_RPC
from app.transaction import process_logs


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


if __name__ == "__main__":
    # asyncio.run(subscribe_solana_logs())
    # asyncio.run(parse_amm_v4_transaction("41VNq84XWKvN8SHnZ6Wd4iawouDxkVorrYN9r4jwszF7v1eFABMFPKwXivEESk3pifrZ8JJs6PEPe6uybNNizANq"))
    asyncio.run(parse_clmm_transaction("63H6V1tSQuwDF1gNsvYBiQuX4uFuBpU2gFxwoJJNHgjeP2uQJbQ5dW8ZwmjctN6kDSLNC8mnpTFo8fzwYT3C8Csf"))
