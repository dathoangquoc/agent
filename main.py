import os
import asyncio

from dotenv import load_dotenv

from agents import enable_verbose_stdout_logging

from app.config import LiteLLMConfig
from app.agent import ChatWithMemory

ENV_PATH = ".prod.env"
        
if __name__ == "__main__":
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    litellm_config = LiteLLMConfig()

    chat_client = ChatWithMemory(
        user_id="Kajiwara",
        model=litellm_config.model,
        api_key=litellm_config.api_key,
    )

    # For debug
    # enable_verbose_stdout_logging()
    asyncio.run(chat_client.start_chat_async())
