import os
import asyncio

from dotenv import load_dotenv

from agents import enable_verbose_stdout_logging

from app.config import Config    
from app.agent import ChatWithMemory
from app.memory import add_mock_memory, mem0_cfg

ENV_PATH = "./.env.local"
        
if __name__ == "__main__":
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    # config = Config.load()
    # config.register_custom_model()

    # chat_client = ChatWithMemory(
    #     user_id="John",
    #     model=f"ollama_chat/{config.MODEL}",
    #     base_url=config.BASE_URL,
    #     api_key=config.API_KEY,
    # )

    # # add_mock_memory()

    # enable_verbose_stdout_logging()
    # asyncio.run(chat_client.start_chat_async())
    
    print(mem0_cfg)