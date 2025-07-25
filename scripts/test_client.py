import os
from dotenv import load_dotenv
from app.client import LiteLLMClient

def main():
    load_dotenv()

    client = LiteLLMClient(
        model=os.environ["MODEL_NAME"],
        api_key=os.environ["API_KEY"],
        base_url=os.environ["BASE_URL"],
        custom_llm_provider="ollama_chat"
    )

    messages = [
        {
            "role": "user",
            "content": "Tell me in a short sentence what can you do"
        }
    ]

    response = client.complete(messages=messages, max_tokens = 100)
    print(response)

if __name__ == "__main__":
    main()