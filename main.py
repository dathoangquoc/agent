import os
from dotenv import load_dotenv
from app.client import LiteLLMClient
from app.config import Config    

ENV_PATH = "./.env.local"

def main():
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    config = Config.load()
    config.register_custom_model()
    
    client = LiteLLMClient(
        model=config.MODEL,
        api_key=config.API_KEY,
        base_url=config.BASE_URL,
        custom_llm_provider=config.CUSTOM_LLM_PROVIDER
    )

    messages = [
        {
            "role": "user",
            "content": "Explain how AI works in a few words"
        }
    ]

    response = client.complete(
        messages=messages,
        debug=True,
        max_tokens = 10000
    ) 

    print(response)

if __name__ == "__main__":
    main()