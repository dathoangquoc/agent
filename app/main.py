import os
import asyncio

# OpenAI Agent

from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    function_tool,
    set_tracing_disabled
)

from mem0 import Memory

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


# Tools
@function_tool
def schedule_meeting(time: str):
    """Schedule a meeting at a chosen time"""
    return f"Meeting has been scheduled at {time}"

@function_tool
def search_document(query: str):
    """Search for a document based on query"""
    return f"No document were found"

@function_tool
def search_web(query: str):
    """Search online sources"""
    return f"Found no info"

# Memory
config = {
    "llm": {

    },
}
m = Memory()

def add_memory(user: str):
    pass

def search_memory(user: str):
    pass

# Agents

model = LitellmModel(model=f"openai/{MODEL_NAME}", base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

agent = Agent(
    name="Main Agent",
    model=model,
    instructions="You are a helpful AI",
    tools=[schedule_meeting, search_document, search_web],
)

async def main():
    result = await Runner.run(agent, "Search for documents on LLM")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
