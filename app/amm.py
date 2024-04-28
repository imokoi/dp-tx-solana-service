from solana.rpc.async_api import AsyncClient
from solders.signature import Signature
from solders.transaction_status import UiTransaction, UiPartiallyDecodedInstruction
from app.common import SOLANA_MAIN_NET_HTTP_RPC

AMM_V4_PROGRAM_INVOKE = "Program 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8 invoke"
AMM_V4_INITIALIZE2 = "Program log: initialize2: InitializeInstruction2"
AMM_POOL_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"


async def pick_amm_v4_initialize2_log(signature: str, logs: list):
    '''
    从日志中提取 AMM V4 的创建提取池子的日志
    '''
    has_amm_v4_program_invoked = False
    has_amm_v4_initialize2 = False
    for log in logs:
        if AMM_POOL_V4_PROGRAM_ID in log:
            has_amm_v4_program_invoked = True
        if AMM_V4_INITIALIZE2 in log:
            has_amm_v4_initialize2 = True

    if not has_amm_v4_program_invoked or not has_amm_v4_initialize2:
        return

    # amm v4 new pool log
    print(f"Amm new Pool created: {signature}")
    await parse_amm_v4_transaction(signature)


async def parse_amm_v4_transaction(signature: str):
    '''
    解析AMM V4的交易相关的 transaction
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
            if str(instruction.program_id) != AMM_POOL_V4_PROGRAM_ID:
                continue

            accounts = instruction.accounts
            pool_id = accounts[4]
            signer = accounts[17]

            print(f"Transaction Signature: {signature}, Block Time: {timestamp}")
            print(f"Pool ID: {pool_id}")
            print(f"Signer: {signer}")

            # TODO 调用 dp-raydium-service 获取详细的池子信息
            break
    except Exception as e:
        # 当tx出错的时候，不需要进行解析
        print(f"Error: {e}")
