import asyncio
import json
import websockets.typing as WebSocketTyping
from solana.rpc.async_api import AsyncClient
from solders.signature import Signature
from solders.transaction_status import UiTransaction, UiPartiallyDecodedInstruction
from app.common import AMM_POOL_V4_PROGRAM_ID, AMM_V4_NEW_POOL_LOG_ID, SOLANA_MAIN_NET_HTTP_RPC


async def process_logs(log_data: WebSocketTyping.Data):
    '''
    解析solana的日志Log消息
    '''
    message_dict = json.loads(log_data)
    try:
        logs = message_dict["params"]["result"]["value"]["logs"]
        signature = message_dict["params"]["result"]["value"]["signature"]

        # amm v4 new pool log
        if AMM_V4_NEW_POOL_LOG_ID in logs:
            print(f"New Pool Created: {signature}")
            asyncio.create_task(parse_amm_v4_transaction(signature))

    except Exception as e:
        print(f"Error: {e}")


async def parse_amm_v4_transaction(signature: str):
    '''
    获取transcation 的详细信息
    '''
    try:
        async_client = AsyncClient(SOLANA_MAIN_NET_HTTP_RPC)
        transaction = await async_client.get_transaction(tx_sig=Signature.from_string(signature), encoding="jsonParsed")
        if not transaction.value:
            return
        timestamp = transaction.value.block_time
        print(f"Transaction Signature: {signature}, Block Time: {timestamp}")

        tx = transaction.value.transaction.transaction
        if not isinstance(tx, UiTransaction):
            return

        for instruction in tx.message.instructions:
            if not isinstance(instruction, UiPartiallyDecodedInstruction):
                continue
            if str(instruction.program_id) != AMM_POOL_V4_PROGRAM_ID:
                continue

            accounts = instruction.accounts
            pool_id = accounts[4]
            signer = accounts[17]

            print(f"Pool ID: {pool_id}")
            print(f"Signer: {signer}")

            # TODO 调用 dp-raydium-service 获取详细的池子信息
            break
    except Exception as e:
        print(f"Error: {e}")
