import os

class Config:
    MODEL_NAME = os.environ["MODEL_NAME"]
    API_KEY = os.environ["API_KEY"]
    BASE_URL = os.environ["BASE_URL"]
    CUSTOM_LLM_PROVIDER = os.environ["CUSTOM_LLM_PROVIDER"]

    if not MODEL_NAME:
        raise ValueError("MODEL_NAME is not set")
    
    if not API_KEY:
        raise ValueError("API_KEY is not set")
    
    if not BASE_URL:
        raise ValueError("BASE_URL is not set")
    
    if not CUSTOM_LLM_PROVIDER:
        raise ValueError("CUSTOM_LLM_PROVIDER is not set")
    