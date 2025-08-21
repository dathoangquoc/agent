import os
import asyncio

from dotenv import load_dotenv

import litellm

from agents import enable_verbose_stdout_logging

from app.config import LiteLLMConfig
from app.agent import ChatWithMemory

        
if __name__ == "__main__":
    ENV_PATH = ".prod.env"
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    litellm.drop_params = True
    litellm.callbacks = ['langfuse_otel']

    litellm_config = LiteLLMConfig()

    chat_client = ChatWithMemory(
        user_id="A",
        session_id=3,
        model=litellm_config.model,
        api_key=litellm_config.api_key,
    )

    # For debug
    # enable_verbose_stdout_logging()
    
    asyncio.run(chat_client.start_chat_async())
