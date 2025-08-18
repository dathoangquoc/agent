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

# Litellm
import litellm

from .memory import create_memory_tools
from app.prompt import MAIN_AGENT_PROMPT

# Enable tracing through litellm client
set_tracing_disabled(True)
litellm.callbacks = ["langfuse_otel"]

class ChatWithMemory:
    def __init__(self, model, base_url, api_key, user_id: str):
        self.user_id = user_id
        self.history = []

        memory_tools = create_memory_tools(chat_instance=self)

        self.starting_agent = Agent(
            name="Main Agent",
            instructions=MAIN_AGENT_PROMPT,
            model=LitellmModel(
                model=model,
                # base_url=base_url,
                api_key=api_key,
            ),
            tools=memory_tools,
        )
        
    async def start_chat_async(self):
        """
        Start a chat loop
        """
        messages = []
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting chat...")
                break

            user_message = {"role": "user", "content": user_input}

            messages.append(user_message)
            self.history.append(user_message)

            result = Runner.run_streamed(self.starting_agent, input=user_input)

            print("Agent: ")
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
            
            response_message = {"role": "assistant", "content": result.final_output}

            messages.append(response_message)
            self.history.append(response_message)
            
            print("-------------------------------------------------------")
        
        
    
    def mock_chat(prev_dialog: str, next_dialog: str):
        """
        Simulate 2 distinct dialog sessions of 1 user 
        """
        pass
