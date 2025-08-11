from uuid import uuid4

# OpenAI Agent
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    set_tracing_disabled,
)

from .memory import add_memory, search_memory
from .message import Message

# TODO: trace with langfuse
class ChatWithMemory:
    def __init__(self, model, base_url, api_key, user_id: str):
        self.user_id = user_id
        self.starting_agent = Agent(
            name="Main Agent",
            instructions="You are a helpful AI",
            model=LitellmModel(
                model=model,
                base_url=base_url,
                api_key=api_key,
            ),
            tools=[search_memory],
        )
        set_tracing_disabled(True)
    
    async def start_chat_loop(self):
        """
        Start a chat loop with user_id, auto session_id

        chat: Runner.run()        

        chat ends -> add(messages)

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

            result = await Runner.run(
                starting_agent=self.starting_agent,
                input=messages,
            )

            print(result.final_output)

        # Save session to memory after ending
        add_memory(
            messages=messages,
            user_id=self.user_id
        )