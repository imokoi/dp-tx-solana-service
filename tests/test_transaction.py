from inspect import signature
from app.amm import parse_amm_v4_transaction
from app.clmm import parse_clmm_transaction
from app.transaction import process_logs
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
async def test_parse_amm_v4_transaction():
    '''
    测试 parse_transaction 函数
    '''
    signature = "5WXz8C15zkXsLtihXaAYHUyg7UtuFYZDVu7CzS8aWq1k3BREphkxBKTSDc3ZQ7GxgUMKQQbPQhUtiTC9DTM2cPVM"
    await parse_amm_v4_transaction(signature)


@pytest.mark.asyncio
async def test_parse_clmm_transaction():
    signature = "63H6V1tSQuwDF1gNsvYBiQuX4uFuBpU2gFxwoJJNHgjeP2uQJbQ5dW8ZwmjctN6kDSLNC8mnpTFo8fzwYT3C8Csf"
    await parse_clmm_transaction(signature)
