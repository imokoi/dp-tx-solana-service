from inspect import signature
from app.transaction import process_logs, parse_amm_v4_transaction
import pytest

# from app.transaction.parser import analyze_solana_logs


@pytest.mark.asyncio
async def test_analyze_solana_logs():
    '''
    测试 analyze_solana_logs 函数
    '''
    print("test_analyze_solana_logs")
    # 读取 json 文件
    with open("./test_log.json", "r") as f:
        message = f.read()
        # print(message)
        await process_logs(message)


@pytest.mark.asyncio
async def test_parse_transaction():
    '''
    测试 parse_transaction 函数
    '''
    signature = "5WXz8C15zkXsLtihXaAYHUyg7UtuFYZDVu7CzS8aWq1k3BREphkxBKTSDc3ZQ7GxgUMKQQbPQhUtiTC9DTM2cPVM"
    await parse_amm_v4_transaction(signature)
