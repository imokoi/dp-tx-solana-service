import asyncio
import json
import websockets.typing as WebSocketTyping
from solana.rpc.async_api import AsyncClient
from solders.signature import Signature
from solders.transaction_status import UiTransaction, UiPartiallyDecodedInstruction
from app.amm import pick_amm_v4_initialize2_log


async def process_logs(log_data: WebSocketTyping.Data):
    '''
    解析solana的日志Log消息
    '''
    message_dict = json.loads(log_data)
    try:
        logs = message_dict["params"]["result"]["value"]["logs"]
        signature = message_dict["params"]["result"]["value"]["signature"]

        # 提取 AMM v4 的创建提取池子的日志
        asyncio.create_task(pick_amm_v4_initialize2_log(signature, logs))
    except Exception as e:
        print(f"Error: {e}")
