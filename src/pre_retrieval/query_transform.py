from dataclasses import dataclass

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from .prompts import QUERY_TRANSFORM_ORCHESTRATOR_PROMPT, QUERY_REWRITE_PROMPT, MULTI_QUERY_GENERATION_PROMPT, HYPOTHETICAL_DOCUMENT_EMBEDDING_PROMPT, EXTRACT_METADATA_PROMPT


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

    def __init__(self, model: str, api_key: str):
        self.llm = LitellmModel(
            model=model,
            api_key=api_key,
        )

        self.rewrite_agent = Agent(
            name="Query Rewrite Agent",
            instructions=str(QUERY_REWRITE_PROMPT),
            model=self.llm,
        )

        self.multi_query_agent = Agent(
            name="Multi Query Generation Agent",
            instructions=str(MULTI_QUERY_GENERATION_PROMPT),
            model=self.llm
        )

        self.hyde_agent = Agent(
            name="HyDE Agent",
            instructions=str(HYPOTHETICAL_DOCUMENT_EMBEDDING_PROMPT),
            model=self.llm
        )

        self.extract_metadata_agent = Agent(
            name="Extract Metadata Agent",
            instructions=str(EXTRACT_METADATA_PROMPT),
            model=self.llm
        )

        self.orchestrator = Agent(
            name="Orchestrator",
            instructions=str(QUERY_TRANSFORM_ORCHESTRATOR_PROMPT),
            tools=[
                self.rewrite_agent.as_tool(
                    tool_name=None,
                    tool_description=None
                ),
                self.multi_query_agent.as_tool(
                    tool_name=None,
                    tool_description=None
                ),
                self.hyde_agent.as_tool(
                    tool_name=None,
                    tool_description=None
                ),
                self.extract_metadata_agent.as_tool(
                    tool_name=None,
                    tool_description=None
                )
            ],
            model=self.llm
        )

    async def process_query(self, query: str):
        """
        Let an Orchestrator Agent decides how to handle the query
        """
        result = await Runner.run(
            starting_agent=self.orchestrator,
            input=query
        )
        return result
