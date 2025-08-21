# OpenAI Agent
import gc
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    set_tracing_disabled
)

import aiohttp
from openai.types.responses import ResponseTextDeltaEvent

from .memory import create_memory_tools

MEMORY_AGENT_PROMPT = """
You are a helpful agent with memory capabilities.
You can search for memories, add new memories related to the user.

If provided with memory of the last session, use it as context and continue the conversation.
"""

# Disable OpenAI tracing
set_tracing_disabled(True)

class ChatWithMemory:
    def __init__(self, model, api_key, user_id: str, session_id: int = 1):
        self.user_id = user_id
        self.session_id = str(session_id - 1)
        self.history = []

        search_memory, add_memory, get_last_session = create_memory_tools(chat_instance=self)
        self.get_last_session = get_last_session

        self.starting_agent = Agent(
            name="Memory Agent",
            instructions=MEMORY_AGENT_PROMPT,
            model=LitellmModel(
                model=model,
                api_key=api_key,
            ),
            tools=[search_memory, add_memory],
        )
        
    async def start_chat_async(self):
        """
        Start a chat loop
        """
        try:
            prev_session = self.get_last_session()
            if prev_session['results'][0]['memory']:
                prev_memory = prev_session['results'][0]['memory']
            messages = [
                {"content": f"Previous session: {prev_memory}", "role": "system"}
            ]
            while True:
                user_input = input("You: ")
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Exiting chat...")
                    break

                user_message = {"content": user_input, "role": "user"}

                messages.append(user_message)
                self.history.append(user_message)

                result = Runner.run_streamed(self.starting_agent, input=messages)

                print("\nAgent: ")
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        print(event.data.delta, end="", flush=True)
                
                response_message = {"content": result.final_output, "role": "assistant"}

                messages.append(response_message)
                self.history.append(response_message)
                
                print("-------------------------------------------------------")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up all unclosed aiohttp sessions"""
        for obj in gc.get_objects():
            if isinstance(obj, aiohttp.ClientSession) and not obj.closed:
                await obj.close()
            

    def mock_chat(prev_dialog: str, next_dialog: str):
        """
        Simulate 2 distinct dialog sessions of 1 user 
        """
        pass
