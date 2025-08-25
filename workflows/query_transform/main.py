from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel


from src.prompt import Prompt

query_rewrite_prompt = Prompt(
    task="Your task is to rewrite the user's query to be more specific and detailed.",
    instructions="You should use the context provided to enhance the user's query.",
    context="The user may provide vague or incomplete queries. Use the context to make the query clearer.",
    role="You are a query rewriting assistant.",
    examples="For example, if the user asks 'What is the weather?', you can rewrite it to 'What is the current weather in New York City?'",
    output_format="Please provide the rewritten query in a clear and concise manner.",
)

query_rewrite_agent = Agent(
    name="Query Transform Agent",
    instructions=query_rewrite_prompt,
    model=LitellmModel(
        model="your-model-name",
        api_key="your-api-key",
    ),
)

initial_agent_prompt = Prompt(
    task="""Your task is to decide if a query:
1. Can be answered immediately
2. Ambiguous, has implied information that needs to be transformed
3. Not enough information to answer""",
    instructions="""
- If the task can be easily answered, do it
- If it is ambiguous, forward the task to the handoff agent  
- Else ask the user to clarify
"""
) 

initial_agent = Agent(
    name="Initial Agent",
    instructions=initial_agent_prompt,
    handoffs=[query_rewrite_agent]
)