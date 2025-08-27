from dataclasses import dataclass

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from .prompts import INITIAL_AGENT_PROMPT, QUERY_REWRITE_PROMPT

@dataclass
class QueryTransformer:
    """
    Input: User query
    Output: Agent decides when and how to transform user query
    Possible methods:
    - Rewrite query to remove ambiguity
    - Generate 5 new semantically-diverse queries
    - Extract metadata
    - Generate hypothetical documents
    """
    pass



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