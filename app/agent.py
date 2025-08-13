from uuid import uuid4

# OpenAI Agent
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    function_tool,
    set_tracing_disabled,
)

from openai.types.responses import ResponseTextDeltaEvent

from .memory import MemoryClient
from .message import Message


# TODO: trace with langfuse
class ChatWithMemory:
    def __init__(self, model, base_url, api_key, user_id: str, memory_client: MemoryClient):
        self.user_id = user_id
        self.memory_client = memory_client
        self.starting_agent = Agent(
            name="Main Agent",
            instructions="You are a helpful AI",
            model=LitellmModel(
                model=model,
                base_url=base_url,
                api_key=api_key,
            ),
            tools=[self.search_memory],
        )
        set_tracing_disabled(True)
    
    @function_tool
    def search_memory(self, query, user_id) -> str:
        """
        Retrieve a memory based on query and user_id
        """
        return self.memory_client.search_memory(query, user_id)


    async def start_chat_async(self):
        """
        Start a chat loop
        """
        messages = []
        session_id = uuid4()
        
        while True:
            print("[User]: ")
            message = Message(
                content=input(),
                role="user"
            )

            if message["content"] in ["q", "quit", "exit"]:
                break
            else:
                messages.append(message)

            result = Runner.run_streamed(
                self.starting_agent,
                messages,
            )
            async for event in result.stream_events():
                if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
            print("\n")

        # Save session to memory after ending
        self.memory_client.add_memory(
            messages=messages,
            user_id=self.user_id
        )
    
    def mock_chat(prev_dialog: str, next_dialog: str):
        """
        Simulate 2 distinct dialog sessions of 1 user 
        """
        pass