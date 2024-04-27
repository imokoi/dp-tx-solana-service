import asyncio
import json
from solana.rpc.async_api import AsyncClient
from solders.signature import Signature
import websockets

SOLANA_MAIN_NET_HTTP_RPC = "https://api.mainnet-beta.solana.com"
SOLANA_MAIN_NET_WS_RPC = "wss://api.mainnet-beta.solana.com"

SOLANA_DEV_NET_HTTP_RPC = "https://api.devnet.solana.com"
SOLANA_DEV_NET_WS_RPC = "wss://api.devnet.solana.com"

AMM_POOL_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
CLMM_POOL_PROGRAM_ID = "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK"


async def connect_ws_rpc():
    async with websockets.connect(SOLANA_DEV_NET_WS_RPC) as websocket:
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
        print(f"Received log: {message}")

        # 循环接收日志消息
        # try:
        #     while True:
        #         message = await websocket.recv()
        #         print(f"Received log: {message}")
        # except websockets.exceptions.ConnectionClosed:
        #     print("Connection with server closed")


async def analyze_message(message: websockets.Data):
    message_dict = json.loads(message)
    print(f"Received message: {message_dict}")
    if "params" not in message_dict:
        return
    if "result" not in message_dict["params"]:
        return
    if "value" not in message_dict["params"]["result"]:
        return
    for log in message_dict["params"]["result"]["value"]["logs"]:
        print(f"Received log: {log}")


async def get_transaction(signature: str):
    '''
    获取transcation 的详细信息
    '''
    async_client = AsyncClient(SOLANA_MAIN_NET_HTTP_RPC)
    transaction = await async_client.get_transaction(tx_sig=Signature.from_string(signature), encoding="jsonParsed")
    print(transaction)


if __name__ == "__main__":
    # asyncio.run(connect_ws_rpc())
    asyncio.run(get_transaction("5WXz8C15zkXsLtihXaAYHUyg7UtuFYZDVu7CzS8aWq1k3BREphkxBKTSDc3ZQ7GxgUMKQQbPQhUtiTC9DTM2cPVM"))
