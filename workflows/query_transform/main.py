import os
import asyncio
import logging
from dotenv import load_dotenv

from src.pre_retrieval.query_transform import QueryTransformer


ENV_PATH = ".prod.env"

if __name__ == "__main__":
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    else:
        print("Not found env")

    transformer = QueryTransformer(
        model=os.environ['MODEL'],
        api_key=os.environ['API_KEY']
    )
    
    # Query needs to be vague for agent to use tool
    query = "What about AI?"
    transformed = asyncio.run(transformer.process_query_parallel(query))
    print(transformed)
