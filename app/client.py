from typing import List, TypedDict, AsyncGenerator

import litellm
from litellm import completion, acompletion, batch_completion
from langfuse import observe, get_client

from .message import ResponseInput, ResponseOutput
from .tracing import TracingClient

class LiteLLMClient():

    def __init__(
            self, 
            model: str, 
            api_key: str, 
            base_url: str, 
            tracing_client: TracingClient,
            custom_llm_provider: str = None,
        ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.custom_llm_provider = custom_llm_provider
        self.tracing_client = tracing_client

        # Drop unsupported params by provider
        litellm.drop_params = True

    @observe(as_type="generation")
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
            **kwargs
        )

        reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
        output_content = response.choices[0].message.content
        debug_content = reasoning_content + "\n\n" + output_content

        self.tracing_client.update_trace(
            model=self.model,
            response=response,
            user_id=user_id,
            session_id=session_id
        )

        if debug:
            return debug_content

        return output_content

    @observe(as_type='generation')
    async def stream(
        self, 
        messages: List[ResponseInput],
        session_id: str = None,
        user_id: str = None, 
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

    @observe(as_type='generation')
    def batch_complete(
        self,
        messages: List[List[ResponseInput]],
        session_id: str = None,
        user_id: str = None,     
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

        self.tracing_client.update_trace(
            model=self.model,
            response=response,
            session_id=session_id,
            user_id=user_id
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