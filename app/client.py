import os
import litellm
from langfuse import observe
from litellm import completion, batch_completion
from dotenv import load_dotenv

load_dotenv()

class LiteLLMClient():

    def __init__(self, model: str, api_key: str, base_url: str, custom_llm_provider: str = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.custom_llm_provider = custom_llm_provider

    @observe
    def complete(
            self, 
            messages: list[dict[str:str]] = [], 
            **kwargs
        ) -> str:

        # read kwargs
        temperature = kwargs.get("temperature", None)
        top_p = kwargs.get("top_p", None)
        max_tokens = kwargs.get("max_tokens", None)
        
        response = completion(
            model=self.model, 
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            base_url=self.base_url,
            api_key=self.api_key,
            custom_llm_provider=self.custom_llm_provider,
        )

        # Handle failure

        # Parse reasoning

        # Parse tool

        return response

    async def stream(self, messages: list[dict[str:str]] = []):
        return completion(model=self.model, messages=messages, stream=True)

    # Multiple call to 1 model
    def batch_complete(self, messages: list[dict[str:str]] = []):
        return batch_completion(model=self.model, messages=messages)