from litellm import completion

class LiteLLMClient():
    
    model: str


    def complete(self, messages: list[dict[str:str]] = []):
        return completion(model=self.model, messages=messages)

    async def stream():
        pass

    def batch_complete():
        pass