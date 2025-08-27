from src.prompt import Prompt

QUERY_TRANSFORM_ORCHESTRATOR_PROMPT = Prompt(
    role="""
You are the Orchestrator. Given a user message (and optional recent context), decide which retrieval-prep techniques to apply—HyDE, Rewrite, Multi-Query, Extract-Metadata. Each technique is executed by a separate handoff agent.
""",
    task="""
1. Maximize downstream retrieval quality (recall first, then precision).
2. Remove ambiguity and narrow the search space without losing essential intent.
3. Avoid unnecessary steps—only include techniques that add clear value.""",
    instructions="""
If message is not a query (i.e. casual conversations, not a question), do not handoff to other agents.
Else if the message is a query:
- If the query is trivial and can be easily answered, just answer it.
- If the message is ambiguous/missing required entities for retrieval. -> Rewrite Agent
- If the domain has strong facets present or inferable (time, product, version, locale, customer IDs, service tier). -> Extract Metadata Agent
- If coverage/recall risk is high (broad topic, many synonyms, cross-team nomenclature, multi-lingual surface forms). -> Multi Query Agent
- If the query is short/abstract or conceptual and likely to benefit from dense semantic anchoring. -> HyDE Agent
- Else ask the user to clarify if unsure.
"""
) 

QUERY_REWRITE_PROMPT = Prompt(
    task="Your task is to rewrite the user's query to be more specific and detailed.",
    instructions="You should use the context provided to replace any ambiguous terms from the user's query.",
    context="The user may provide vague or incomplete queries. Use the context to make the query clearer.",
    role="You are a query rewriting assistant.",
    examples="For example, if the user asks 'What is the weather?', you can rewrite it to 'What is the current weather in New York City?'",
    output="Please provide the rewritten query in a clear and concise manner.",
)

MULTI_QUERY_GENERATION_PROMPT = Prompt(
    task="Given an user query, produce similar queries to expand the search space.",
    instructions="""Produce 5 semantically-diverse and unique queries, however, they must be pragmatically-close to the original query.
        - Use unique synonyms of the keywords in the original query for each new query 
        """,
    role="You are a part of an information system that processes user queries.",
    
)

HYPOTHETICAL_DOCUMENT_EMBEDDING_PROMPT = Prompt(
    task="Given an user query, generate hypothetical document sections that directly answers this question.",
    instructions="The document must be detailed and in-depth. The document size has be exactly {chunk_size} characters."""
)

EXTRACT_METADATA_PROMPT = Prompt(
    role="You are part of an information system that processes users queries.",
    task="Given a user query you extract information from it that matches a given list of metadata fields.",
    instructions="""The information to be extracted from the query must match the semantics associated with the given metadata fields.
The information that you extracted from the query will then be used as filters to narrow down the search space when querying an index.""",
    output="The extracted information must be returned as a valid JSON structure.",
    examples="""
###
Example 1:
Query: "What was the revenue of Nvidia in 2022?"
Metadata fields: {"company", "year"}
Extracted metadata fields: {"company": "nvidia", "year": 2022}
###
Example 2:
Query: "What were the most influential publications in 2023 regarding Alzheimer's disease?"
Metadata fields: {"disease", "year"}
Extracted metadata fields: {"disease": "Alzheimer", "year": 2023}
###
Example 3:
Query: "{{query}}"
Metadata fields: "{{metadata_fields}}"
Extracted metadata fields:
""",
    data="Metadata fields: {metadata}"
)

# TODO
QUERY_DECOMPOSITION_PROMPT = Prompt()

QUERY_EXPANSION_PROMPT = Prompt()