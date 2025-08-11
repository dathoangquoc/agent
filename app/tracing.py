from abc import ABC, abstractmethod
from typing import Required, Optional, Any

from langfuse import get_client

class TracingClient(ABC):
    @abstractmethod
    def update_trace(self, model: str, response: str, session_id: str = None, user_id: str = None):
        pass

class LangfuseClient(TracingClient):
    def __init__(self):
        self.client = get_client()
        
    def update_trace(self, model, response, session_id: str, user_id: str):
        self.client.update_current_trace(session_id=session_id)
        self.client.update_current_trace(user_id=user_id)
        self.client.update_current_generation(
            model=model,
            usage_details={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            metadata={
                'finish_reason': response.choices[0].finish_reason
            }
        )
    
    def update_trace_stream(self, model, response: str, session_id: str, user_id: str):
        self.client.update_current_trace(session_id=session_id)
        self.client.update_current_trace(user_id=user_id)
        self.client.update_current_generation(
            model=model,
            
        )