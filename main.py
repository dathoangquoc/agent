import os
import asyncio

from dotenv import load_dotenv

from app.config import Config    
from app.agent import ChatWithMemory
from app.memory import MemoryClient

ENV_PATH = "./.env.local"
        
if __name__ == "__main__":
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    config = Config.load()
    config.register_custom_model()

    memory_client = MemoryClient()

    chat_client = ChatWithMemory(
        user_id="John",
        model=f"ollama_chat/{config.MODEL}",
        base_url=config.BASE_URL,
        api_key=config.API_KEY,
        memory_client=memory_client
    )
    asyncio.run(chat_client.start_chat_async())
    