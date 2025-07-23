from litellm import completion, batch_completion

class LiteLLMClient():
    
    model: str
    api_key: str

    def complete(self, messages: list[dict[str:str]] = []):
        # TODO: prepare input: sampling options, custom_llm_provider, model
        
        response = completion(
            model=self.model, 
            messages=messages,
        )

        # TODO: handle failure, reasoning, tool, logging
        return response

    async def stream(self, messages: list[dict[str:str]] = []):
        return completion(model=self.model, messages=messages, stream=True)

    # Multiple call to 1 model
    def batch_complete(self, messages: list[dict[str:str]] = []):
        return batch_completion(model=self.model, messages=messages)