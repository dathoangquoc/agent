import os
import litellm
import asyncio
from typing import List, TypedDict, AsyncGenerator
from langfuse import observe
from litellm import completion, acompletion, batch_completion
from dotenv import load_dotenv

load_dotenv()

class Message(TypedDict):
    role: str
    content: str

class LiteLLMClient():

    def __init__(self, model: str, api_key: str, base_url: str, custom_llm_provider: str = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.custom_llm_provider = custom_llm_provider

    @observe
    def complete(
            self, 
            messages: List[Message], 
            **kwargs
        ):
        
        response = completion(
            model=self.model, 
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            **kwargs
        )

        reasoning = response.choices[0].message.reasoning_content or ""
        reply = response.choices[0].message.content

        return {
            "content": reply,
            "reasoning_content": reasoning
        }

    @observe
    async def stream(
        self, 
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator:
        response = await acompletion(
            model=self.model,
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            stream=True,
            **kwargs
        )

        async for chunk in response:
            reply = chunk.choices[0].delta.content
            if reply:
                yield reply
        

    # Multiple call to 1 model
    def batch_complete(self, messages: List[Message]):
        return batch_completion(model=self.model, messages=messages)
    
async def main():
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

    async for chunk in client.stream(messages, max_tokens=1000):
        print(chunk, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(main())

