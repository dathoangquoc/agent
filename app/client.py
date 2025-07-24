from litellm import completion, batch_completion

class LiteLLMClient():
    
    model: str
    api_key: str
    base_url: str
    custom_llm_provider: str = None

    def complete(
            self, 
            messages: list[dict[str:str]] = [], 
            temperature: float = None,
            top_p: float = None,
            max_tokens: int = None,
        ) -> str:
        
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

        # Logging:
        # https://docs.litellm.ai/docs/completion/token_usage
        # https://docs.litellm.ai/docs/observability/callbacks

        return response

    async def stream(self, messages: list[dict[str:str]] = []):
        return completion(model=self.model, messages=messages, stream=True)

    # Multiple call to 1 model
    def batch_complete(self, messages: list[dict[str:str]] = []):
        return batch_completion(model=self.model, messages=messages)