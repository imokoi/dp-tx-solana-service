from solana.rpc.async_api import AsyncClient
from solders.signature import Signature
from solders.transaction_status import UiTransaction, UiPartiallyDecodedInstruction

from app.common import SOLANA_MAIN_NET_HTTP_RPC

CLMM_PROGRAM_INVOKE = "Program CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK invoke"
CLMM_PROGRAM_CREATE_POOL_INSTRUCTION = "Program log: Instruction: CreatePool"
CLMM_POOL_PROGRAM_ID = "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK"


async def pick_clmm_create_pool_instruction_log(signature: str, logs: list):
    '''
    从日志中提取 CLMM 的创建提取池子的日志
    '''
    has_clmm_program_invoked = False
    has_clmm_create_pool_instruction = False
    for log in logs:
        if CLMM_PROGRAM_INVOKE in log:
            has_clmm_program_invoked = True
        if CLMM_PROGRAM_CREATE_POOL_INSTRUCTION in log:
            has_clmm_create_pool_instruction = True

    if not has_clmm_program_invoked or not has_clmm_create_pool_instruction:
        return

    # clmm new pool log
    print(f"Clmm new pool created: {signature}")
    await parse_clmm_transaction(signature)


async def parse_clmm_transaction(signature: str):
    '''
    解析CLMM的交易相关的 transaction
    '''
    try:
        async_client = AsyncClient(SOLANA_MAIN_NET_HTTP_RPC)
        transaction = await async_client.get_transaction(
            tx_sig=Signature.from_string(signature),
            encoding="jsonParsed",
            max_supported_transaction_version=0
        )
        if not transaction.value:
            return
        timestamp = transaction.value.block_time

        tx = transaction.value.transaction.transaction
        if not isinstance(tx, UiTransaction):
            return

        for instruction in tx.message.instructions:
            if not isinstance(instruction, UiPartiallyDecodedInstruction):
                continue
            if str(instruction.program_id) != CLMM_POOL_PROGRAM_ID:
                continue

            accounts = instruction.accounts
            pool_id = accounts[2]
            signer = accounts[0]

            print(f"Transaction Signature: {signature}, Block Time: {timestamp}")
            print(f"Pool ID: {pool_id}")
            print(f"Signer: {signer}")

            # TODO 调用 dp-raydium-service 获取详细的池子信息
            break
    except Exception as e:
        # 当tx出错的时候，不需要进行解析
        print(f"Error: {e}")
