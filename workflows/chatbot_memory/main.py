import os
import sys
import asyncio
from dotenv import load_dotenv

import litellm
from agents import enable_verbose_stdout_logging
from mem0 import Memory

from src.config import LiteLLMConfig, mem0_cfg
from .chatbot_memory import ChatWithMemory


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    ENV_PATH = ".prod.env"
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    litellm.drop_params = True
    litellm.callbacks = ['langfuse_otel']

    litellm_config = LiteLLMConfig()

    memory_client = Memory.from_config(mem0_cfg)
    chat_client = ChatWithMemory(
        user_id="A",
        session_id=1,
        model=litellm_config.model,
        api_key=litellm_config.api_key,
    )

    # For debug
    enable_verbose_stdout_logging()
    
    asyncio.run(chat_client.start_chat_async())
