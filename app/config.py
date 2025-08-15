import os
import litellm
from yaml import safe_load

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

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

# Component Configs
class LLMConfig(BaseModel):
    model: str
    provider: str
    api_key: str
    base_url: str

class EmbedderConfig(BaseModel):
    model: str
    provider: str
    api_key: str
    base_url: str
    embedding_model_dims: int

class VectorStoreConfig(BaseModel):
    provider: str
    host: str
    port: int
    collection_name: str
    
# Service Configs

class Mem0Config(BaseSettings):
    vector_store: VectorStoreConfig
    llm: LLMConfig
    embedder: EmbedderConfig

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 1024, 
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "gemma3:4b",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434", 
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "snowflake-arctic-embed2",
            "ollama_base_url": "http://localhost:11434",
        },
    },
}