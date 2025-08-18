import os
import litellm
from yaml import safe_load

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LiteLLMConfig(BaseSettings):
    model: str = Field(..., description="The model to use for LiteLLM")
    base_url: str = Field(..., description="Base URL for the LiteLLM API")
    api_key: str = Field(..., description="API key for LiteLLM access")
    custom_llm_provider: str = Field("openai", description="Custom LLM provider name")
    
def register_custom_model():
    litellm.register_model({
        "qwen3:4b": {
            "input_cost_per_token": 0.00000000011,
            "output_cost_per_token": 0.00000000126,
        }
    })

### Configs
class LLMConfig(BaseModel):
    model: str

class EmbedderConfig(BaseModel):
    model: str

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
