import os
import litellm
from yaml import safe_load

from pydantic_settings import BaseSettings

class Config:
    MODEL: str
    API_KEY: str
    BASE_URL: str
    CUSTOM_LLM_PROVIDER: str = None
    
    def __init__(self, model, api_key, base_url, custom_llm_provider=None):
        self.MODEL = model
        self.API_KEY = api_key
        self.BASE_URL = base_url
        self.CUSTOM_LLM_PROVIDER = custom_llm_provider

    @classmethod
    def load(cls):
        model = os.environ["MODEL"]
        api_key = os.environ["API_KEY"]
        base_url = os.environ["BASE_URL"]
        custom_llm_provider = os.environ["CUSTOM_LLM_PROVIDER"]
    
        if not model:
            raise ValueError("MODEL is not set")
        
        if not api_key:
            raise ValueError("API_KEY is not set")
        
        if not base_url:
            raise ValueError("BASE_URL is not set")
    
        return cls(
            model=model,
            api_key=api_key,
            base_url=base_url,
            custom_llm_provider=custom_llm_provider
        )
    
    def register_custom_model(self):
        litellm.register_model({
            "qwen3:4b": {
                "input_cost_per_token": 0.00000000011,
                "output_cost_per_token": 0.00000000126,
            }
        })


"""1. ModelConfig():
    provider 
....



config -> load() -> ModelConfig instances 



2. ModelManager():
    register(model_config):

    get()"""

with open('config.yml', 'r') as f:
    base_cfg = safe_load(f)

class LiteLLMConfig(BaseSettings):
    model: str
    api_key: str
    base_url: str
    custom_llm_provider: str = None

class Mem0Config(BaseSettings):
    pass

# Instantiate

litellm_cfg = LiteLLMConfig(
    model=base_cfg['']
)