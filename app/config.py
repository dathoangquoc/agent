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

# Component Configs
class LLMConfig(BaseModel):
    model: str
    api_key: str
    base_url: str

class EmbedderConfig(BaseModel):
    model: str
    api_key: str
    base_url: str
    embedding_model_dims: int

class VectorStoreConfig(BaseModel):
    host: str
    port: int
    collection_name: str
    
# Service Configs
class LLM(BaseModel):
    provider: str
    config: LLMConfig

class Embedder(BaseModel):
    provider: str
    config: EmbedderConfig

class VectorStore(BaseModel):
    provider: str
    config: VectorStoreConfig

# Module Configs
class Mem0Config(BaseSettings):
    vector_store: VectorStore
    llm: LLM
    embedder: Embedder

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        yaml_file="mem0.yaml",
    )
