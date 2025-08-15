import os
import asyncio

from dotenv import load_dotenv

from agents import enable_verbose_stdout_logging

from app.config import Config, Mem0Config
from app.agent import ChatWithMemory

ENV_PATH = "./test.env"
        
if __name__ == "__main__":
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    config = Config.load()
    config.register_custom_model()

    chat_client = ChatWithMemory(
        user_id="John",
        model=f"{config.CUSTOM_LLM_PROVIDER}/{config.MODEL}",
        base_url=config.BASE_URL,
        api_key=config.API_KEY,
    )

    # add_mock_memory()

    enable_verbose_stdout_logging()
    asyncio.run(chat_client.start_chat_async())
