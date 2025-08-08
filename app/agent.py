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
    GuardrailFunctionOutput,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrailTripwireTriggered
)

from mem0 import Memory

memory = Memory()

@function_tool
def search_memories(message: str, user_id: str) -> str:
    """Search for user memories

    Args:
        message: user's message
        user_id: user ID
    """
    relevant_memories = memory.search(message, user_id, limit=3)
    formatted_memories = "\n".join([f"{entry['memory']}" for entry in relevant_memories["results"]])

    return formatted_memories

# Agents

model = LitellmModel(model=f"openai/{MODEL_NAME}", base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

### Main Agent

main_agent = Agent(
    name="Main Agent",
    instructions="You are a helpful AI",
    model=model,
    tools=[search_memories],
)