import os
import uuid
import asyncio

from dotenv import load_dotenv

from src.client import LiteLLMClient
from src.config import Config    
from src.tracing.tracing import LangfuseClient

ENV_PATH = "./.env.local"

async def chat_loop(client: LiteLLMClient):
    print("Enter User ID: ")
    user_id = input()
    session_id = uuid.uuid4()
    messages = []

    while True:
        print("[User]: ")
        user_message = input()

        if user_message.lower() == "quit":
            break

        messages.append({
            "role": "user",
            "content": f"{user_message}"
        })

        print("[Assistant]: ", end="")
        assistant_message = ""
        
        async for chunk in client.stream(
            messages=messages,
            max_tokens = 10000,
            user_id= user_id,
            session_id=session_id
        ):
            assistant_message += chunk
            print(chunk, end="", flush=True)

        messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        print("\n\n")

def completion_test(client: LiteLLMClient):
    messages = [
        {
            "role": "user",
            "content": "Explain how AI works in a few words"
        }
    ]

    response = client.complete(
        messages=messages,
        debug=True,
        session_id="X",
        user_id="X",
        max_tokens = 100,
        top_p = 0.3,
        reasoning_effort = 'low',
        temperature = 0.2
        ) 

    print(response)

def batch_completion_test(client: LiteLLMClient):
    messages_list = [
        [
            {
                "role": "user",
                "content": "Explain how AI works in a few words"
            }   
        ],
        [
            {
                "role": "user",
                "content": "Explain how Machine Learning works in a few words"
            }   
        ],
        [
            {
                "role": "user",
                "content": "Explain how Computer Vision works in a few words"
            }   
        ]
    ]

    for response in client.batch_complete(
        messages=messages_list,
        debug=True,
        session_id="1",
        user_id="1",
        max_completion_tokens=500,
        max_tokens=100,
        top_p=0.3,
        reasoning_effort = 'low',
        temperature = 0.2,
    ):
        print(response)
        
if __name__ == "__main__":
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
        custom_llm_provider=config.CUSTOM_LLM_PROVIDER,
    )

    # asyncio.run(chat_loop(client))
    completion_test(client)
    # batch_completion_test(client)