from typing import List, TypedDict, AsyncGenerator

import litellm
from litellm import completion, acompletion, batch_completion
from langfuse import get_client

from .message import ResponseInput, ResponseOutput


class LiteLLMClient():

    def __init__(
            self, 
            model: str, 
            api_key: str, 
            base_url: str, 
            custom_llm_provider: str = None,
        ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.custom_llm_provider = custom_llm_provider

        # Drop unsupported params by provider
        litellm.drop_params = True
        litellm.callbacks = ['langfuse_otel']

    def complete(
            self, 
            messages: List[ResponseInput],
            debug: bool = None,
            session_id: str = None,
            user_id: str = None, 
            **kwargs
        ) -> ResponseOutput:
        response = completion(
            model=self.model, 
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            metadata={
                "session_id": session_id,
                "user_id": user_id
            }
            **kwargs
        )

        reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
        output_content = response.choices[0].message.content
        debug_content = reasoning_content + "\n\n" + output_content

        if debug:
            return debug_content

        return output_content

    async def stream(
        self, 
        messages: List[ResponseInput],
        session_id: str,
        user_id: str, 
        **kwargs
    ) -> AsyncGenerator:
        response = await acompletion(
            model=self.model,
            messages=messages,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
            stream=True,
            metadata={
                "session_id": session_id,
                "user_id": user_id
            }
            **kwargs
        )

        content = ""
        async for chunk in response:
            reply = chunk.choices[0].delta.content
            if reply:
                content += reply
                yield reply
        
        # TODO: Custom callback https://docs.litellm.ai/docs/observability/custom_callback#custom-callback-to-track-costs-for-streaming--non-streaming

    def batch_complete(
        self,
        messages: List[List[ResponseInput]],
        session_id: str,
        user_id: str,     
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
            reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
            output_content = response.choices[0].message.content
            debug_content = reasoning_content + "\n\n" + output_content

            replies.append(debug_content) 

        return replies