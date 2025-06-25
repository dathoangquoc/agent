import os
import asyncio

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
def search_document(query: str):
    """Search for a document based on query"""
    return f"No document were found"

@function_tool
def search_web(query: str):
    """Search online sources"""
    return f"Found no info"

# TODO: mem0 config
config = {
    "llm": {

    },
}
# m = Memory()

def add_memory(user: str):
    pass

def search_memory(user: str):
    pass

# Agents

model = LitellmModel(model=f"openai/{MODEL_NAME}", base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(True)

### Guardrail
guardrail_agent = Agent(
    name="Input Guardrail",
    instructions="Check if the user is asking questions unrelated to the career service",
    model=model,
)

class CareerServiceOutput():
    reasoning: str
    is_career_inquiry: bool


@input_guardrail
async def career_guardrail(
    agent: Agent, input: str | list[TResponseInputItem], context: RunContextWrapper[None]
) -> GuardrailFunctionOutput:
    """Check if the input is unrelated to the career service
    """
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
    handoffs=[],
    input_guardrails=[career_guardrail],
    tools=[schedule_meeting, search_document, search_web],
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
