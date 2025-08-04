import os
import litellm
import asyncio
from typing import List, TypedDict, AsyncGenerator
from langfuse import observe, get_client
from litellm import completion, acompletion, batch_completion
from .message import ResponseInput, ResponseOutput

class LiteLLMClient():

    def __init__(self, model: str, api_key: str, base_url: str, custom_llm_provider: str = None, ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.custom_llm_provider = custom_llm_provider

        # Drop unsupported params by provider
        litellm.drop_params = True
        litellm.callbacks = ["langfuse_otel"]

    def complete(
            self, 
            messages: List[ResponseInput],
            debug: bool = None, 
            **kwargs
        ) -> ResponseOutput:
        
        response = completion(
            model=self.model, 
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            **kwargs
        )

        reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
        output_content = response.choices[0].message.content

        if debug:
            return reasoning_content + "\n\n" + output_content

        return output_content

    async def stream(
        self, 
        messages: List[ResponseInput],
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

    def batch_complete(
        self,
        messages: List[List[ResponseInput]],
        **kwargs
    ) -> List[ResponseOutput]:
        responses = batch_completion(
            model=self.model,
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            **kwargs
        )

        replies = []
        for response in responses:
            replies.append(
                {
                    "content": response.choices[0].message.content,
                    "reasoning_content": getattr(response.choices[0].message, "reasoning_content", "")
                }
            ) 

        return replies
    
### TEST

async def stream_test(client):
    messages = [
        {
            "role": "user",
            "content": "Tell me in a short sentence what can you do"
        }
    ]

    async for chunk in client.stream(messages, max_tokens=1000):
        print(chunk, end='', flush=True)

def batch_test(client):
    messages_list = [
        [
            {
                "role": "user",
                "content": "Tell me in a short sentence what can you do"
            }
        ],
        [
            {
                "role": "user",
                "content": "Good morning"
            }
        ]
    ]

    replies = client.batch_complete(messages_list)
    for reply in replies:
        print(reply)

