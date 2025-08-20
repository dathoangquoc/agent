from typing import List, AsyncGenerator

from dataclasses import dataclass
import litellm
from litellm import completion, acompletion, batch_completion

from .message import ResponseInput, ResponseOutput

@dataclass
class LiteLLMClient():
    model: str
    api_key: str
    base_url: str
    custom_llm_provider: str

    def complete(
            self, 
            messages: List[ResponseInput],
            debug: bool = None,
            session_id: str = None,
            user_id: str = None, 
            **kwargs
        ) -> ResponseOutput:
        try:
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
        except Exception as e:
            print(f"Error during completion: {e}")
            return "Error during completion"

        reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
        output_content = response.choices[0].message.content
        debug_content = reasoning_content + "\n\n" + output_content

        if debug:
            return debug_content

        return output_content

    # TODO: fix session_id w/ older versions of langfuse
    async def stream(
        self, 
        messages: List[ResponseInput],
        session_id: str,
        user_id: str, 
        **kwargs
    ) -> AsyncGenerator:
        try:
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
        except Exception as e:
            print(f"Error during streaming: {e}")
            yield "Error during streaming"
            return

        content = ""
        async for chunk in response:
            reply = chunk.choices[0].delta.content
            if reply:
                content += reply
                yield reply
        
    def batch_complete(
        self,
        messages: List[List[ResponseInput]],
        session_id: str,
        user_id: str,     
        **kwargs
    ) -> List[ResponseOutput]:
        try:
            responses = batch_completion(
                model=self.model,
                messages=messages,
                base_url=self.base_url,
                api_key=self.api_key,
                custom_llm_provider=self.custom_llm_provider,
                **kwargs
            )
        except Exception as e:
            print(f"Error during batch completion: {e}")
            return ["Error during batch completion"]

        replies = []
        for response in responses: 
            reasoning_content = getattr(response.choices[0].message, "reasoning_content", "")
            output_content = response.choices[0].message.content
            debug_content = reasoning_content + "\n\n" + output_content

            replies.append(debug_content) 

        return replies