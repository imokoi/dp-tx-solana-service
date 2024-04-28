import asyncio
# from app.solana_log import subscribe_solana_logs
from app.websocket import start_websocket_server


if __name__ == "__main__":
    asyncio.run(start_websocket_server())
    # asyncio.run(subscribe_solana_logs())
    # asyncio.run(parse_amm_v4_transaction("41VNq84XWKvN8SHnZ6Wd4iawouDxkVorrYN9r4jwszF7v1eFABMFPKwXivEESk3pifrZ8JJs6PEPe6uybNNizANq"))
    # asyncio.run(parse_clmm_transaction("63H6V1tSQuwDF1gNsvYBiQuX4uFuBpU2gFxwoJJNHgjeP2uQJbQ5dW8ZwmjctN6kDSLNC8mnpTFo8fzwYT3C8Csf"))
