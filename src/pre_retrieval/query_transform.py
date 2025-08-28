import asyncio

from agents import Agent, Runner, ModelSettings, RunResult, ToolCallOutputItem
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
                    tool_description=None,
                    custom_output_extractor=self.extract_agent_output
                ),
                self.multi_query_agent.as_tool(
                    tool_name=None,
                    tool_description=None,
                    custom_output_extractor=self.extract_agent_output
                ),
                self.hyde_agent.as_tool(
                    tool_name=None,
                    tool_description=None,
                    custom_output_extractor=self.extract_agent_output
                ),
                self.extract_metadata_agent.as_tool(
                    tool_name=None,
                    tool_description=None,
                    custom_output_extractor=self.extract_agent_output
                )
            ],
            model=self.llm,
            model_settings=ModelSettings(tool_choice="required")
        )

    # TODO parse each tool call separately
    async def process_query(self, query: str):
        """
        Let an Orchestrator Agent decides how to handle the query
        """
        result = await Runner.run(
            starting_agent=self.orchestrator,
            input=query
        )

        items = []
        for item in result.new_items:
            if hasattr(item.raw_item, 'content'):
                items.append(str(item.raw_item.content[0].text))

        return '\n\n'.join(items)
    
    async def process_query_parallel(self, query: str):
        """
        Run all query transformation agents in parallel
        """
        rewrite_result, multi_query_result, hyde_result, extract_metadata_result = await asyncio.gather(
            Runner.run(self.rewrite_agent, query),
            Runner.run(self.multi_query_agent, query),
            Runner.run(self.hyde_agent, query),
            Runner.run(self.extract_metadata_agent, query)
        )

        results = []
        if rewrite_result.final_output:
            results.append(f"Rewritten Query:\n{rewrite_result.final_output}")
        if multi_query_result.final_output:
            results.append(f"Multi Queries:\n{multi_query_result.final_output}")
        if hyde_result.final_output:
            results.append(f"HyDE Document:\n{hyde_result.final_output}")
        if extract_metadata_result.final_output:
            results.append(f"Extracted Metadata:\n{extract_metadata_result.final_output}")

        return '\n\n'.join(results)

    async def extract_agent_output(run_result: RunResult):
        for item in reversed(run_result.new_items):
            if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith('{'):
                print(item.output.strip())
                