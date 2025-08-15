from uuid import uuid4

# OpenAI Agent
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    run_demo_loop,
    set_tracing_disabled
)

from openai.types.responses import ResponseTextDeltaEvent

import litellm

from .memory import search_memory
from .message import Message 


# Enable tracing through litellm client
set_tracing_disabled(True)
litellm.callbacks = ["langfuse_otel"]

class ChatWithMemory:
    def __init__(self, model, base_url, api_key, user_id: str):
        self.user_id = user_id
        self.starting_agent = Agent(
            name="Main Agent",
            instructions="You are a helpful AI, answer any queries when you can. If the user ask about previous interactions, use available tool",
            model=LitellmModel(
                model=model,
                # base_url=base_url,
                api_key=api_key,
            ),
            tools=[search_memory],
        )
        
    async def start_chat_async(self):
        """
        Start a chat loop
        """
        await run_demo_loop(self.starting_agent)

    
    def mock_chat(prev_dialog: str, next_dialog: str):
        """
        Simulate 2 distinct dialog sessions of 1 user 
        """
        pass
