from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from .prompts import INITIAL_AGENT_PROMPT, QUERY_REWRITE_PROMPT


rewrite_agent = Agent(
    name="Query Rewrite Agent",
    instructions=QUERY_REWRITE_PROMPT,
    model=LitellmModel(
        model="your-model-name",
        api_key="your-api-key",
    ),
)

hyde_agent = Agent()




initial_agent = Agent(
    name="Initial Agent",
    instructions=INITIAL_AGENT_PROMPT,
    handoffs=[rewrite_agent]
)