from dotenv import load_dotenv
from app.client import LiteLLMClient
from app.config import Config

def main():
    load_dotenv()

    client = LiteLLMClient(
        model=Config.MODEL_NAME,
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL,
        custom_llm_provider=Config.CUSTOM_LLM_PROVIDER
    )

    messages = [
        {
            "role": "user",
            "content": "Tell me in a short sentence what can you do"
        }
    ]

    print(client.complete(messages=messages, debug=True))

if __name__ == "__main__":
    main()