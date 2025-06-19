import os
import asyncio

from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    function_tool,
    set_tracing_disabled
)

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Agent

model = LitellmModel(model=f"openai/{MODEL_NAME}", base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

@function_tool
def schedule_meeting(time: str):
    """Schedule a meeting at a chosen time"""
    return f"Meeting has been scheduled at {time}"

@function_tool
def retrieve_document(query: str):
    """Search for a document based on query"""
    return f"No document were found"

instructions = "You are a helpful AI."

# Memory

async def main():
    agent = Agent(
        name="Main Agent",
        model=model,
        instructions=instructions,
        tools=[schedule_meeting, retrieve_document],
    )

    result = await Runner.run(agent, "Search for documents on LLM")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
