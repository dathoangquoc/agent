from dotenv import load_dotenv
from app.client import LiteLLMClient
from app.config import Config

class main():
    load_dotenv()

    client = LiteLLMClient(
        model=Config.MODEL_NAME,
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL,
        custom_llm_provider=Config.CUSTOM_LLM_PROVIDER
    )