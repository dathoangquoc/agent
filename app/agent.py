import os
import asyncio
from dataclasses import dataclass
from random import randint

# Pydantic
from pydantic import BaseModel

# OpenAI Agent
from agents.extensions.models.litellm_model import LitellmModel
from agents import (
    Agent, 
    Runner, 
    function_tool,
    set_tracing_disabled,
)

from .config import Config
from .memory import MemoryClient


class ChatWithMemory:
    def __init__(self):
        self.memory_client = MemoryClient()
        self.starting_agent = Agent(
            name="Main Agent",
            instructions="Recall from memory facts about the user to answer query",
            model=LitellmModel(
                model=Config.MODEL,
                base_url=Config.BASE_URL,
                api_key=Config.API_KEY,
            ),
            tools=[self.search_memory]
        )
    
    # Agent Tools
    @function_tool
    def search_memory(self, query: str, user_id: str):
        """
        Search for user memories

        Args:
            query: the search query
            user_id: user ID
        """
        
        relevant_memories=self.memory_client.search_memory(
            query=query,
            user_id=user_id
        )

        formatted_memories="\n".join([f"{entry['memory']}" for entry in relevant_memories["results"]])
        return formatted_memories

    async def run(self, messages):
        result = await Runner.run(
            starting_agent=self.starting_agent,
            input=[messages]
        )

        print(result)