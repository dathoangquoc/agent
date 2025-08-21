# OpenAI Agent
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    set_tracing_disabled
)

from openai.types.responses import ResponseTextDeltaEvent

from .memory import create_memory_tools

MEMORY_AGENT_PROMPT = """
You are a helpful agent with memory capabilities.
You can search for memories, add new memories related to the user.

If provided with memory of the last session, use it as context for the current conversation.
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
            messages = [
                {"role": "system", "content": f"Previous session: {self.get_last_session(query='Any')}"},
            ]
            while True:
                user_input = input("You: ")
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Exiting chat...")
                    break

                user_message = {"role": "user", "content": user_input}

                messages.append(user_message)
                self.history.append(user_message)

                result = Runner.run_streamed(self.starting_agent, input=messages)

                print("\nAgent: ")
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        print(event.data.delta, end="", flush=True)
                
                response_message = {"role": "assistant", "content": result.final_output}

                messages.append(response_message)
                self.history.append(response_message)
                
                print("-------------------------------------------------------")
        finally:
            # BUG: 
            # Unclosed client session
            # client_session: <aiohttp.client.ClientSession object at 0x7a2981fe46b0>
            pass

    def mock_chat(prev_dialog: str, next_dialog: str):
        """
        Simulate 2 distinct dialog sessions of 1 user 
        """
        pass
