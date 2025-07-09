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

# mem0

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
def search_jobs(query: str):
    """Search for a jobs based on a query"""
    return f"No jobs found"

# TODO: add mem0 config
config = {
    "llm": {

    },
}

# memory = Memory()

# @function_tool
# def search_memories(message: str, user_id: str) -> str:
#     """Search for user memories

#     Args:
#         message: user's message
#         user_id: user ID
#     """
#     relevant_memories = memory.search(message, user_id, limit=3)
#     formatted_memories = "\n".join([f"{entry['memory']}" for entry in relevant_memories["results"]])

#     return formatted_memories

# @function_tool
# def add_memories(messages: list[dict[str, str]], user_id: str):
#     """Add new messages to user memories

#     Args:
#         messages: list of messages in the current conversation
#         user_id: user ID
#     """
#     memory.add(messages, user_id)

# Agents

model = LitellmModel(model=f"openai/{MODEL_NAME}", base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

job_search_agent = Agent(
    name="Job Recommendation Agent",
    instructions="Search for suitable jobs for the user",
    model=model,
    tools=[search_jobs]
)

cv_review_agent = Agent(
    name="Job Recommendation Agent",
    instructions="Review the user CV",
    model=model,
)

# Guardrail
class CareerServiceOutput(BaseModel):
    reasoning: str
    is_career_inquiry: bool

guardrail_agent = Agent(
    name="Input Guardrail",
    instructions="Check if the user is asking questions unrelated to the career service",
    model=model,
    output_type=CareerServiceOutput
)

@input_guardrail
async def career_guardrail(
    agent: Agent, input: str | list[TResponseInputItem], context: RunContextWrapper[None]
) -> GuardrailFunctionOutput:
    
    result = await Runner.run(agent, input, context=context)
    final_output = result.final_output_as(CareerServiceOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_career_inquiry
    )

### Main Agent

triage_agent = Agent(
    name="Triage Agent",
    instructions="Handoff to the appropriate agent based on the user's requested service(s)",
    model=model,
    handoffs=[job_search_agent, cv_review_agent],
    # input_guardrails=[career_guardrail],
    # tools=[schedule_meeting, search_document, search_web],
)


async def main():
    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Enter a message: ")
        input_data.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        try:
            result = await Runner.run(triage_agent, input_data)
            print(result.final_output)
        except InputGuardrailTripwireTriggered:
            message = "Sorry I can't help with unrelated inquiries"
            print(message)
            input_data.append(
                {
                    "role": "assistant",
                    "content": message
                }
            )

if __name__ == "__main__":
    asyncio.run(main())
