import os
import asyncio
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
    
    query = "What is Nvidia biggest innovation?"
    transformed = asyncio.run(transformer.process_query(query))
    print(transformed)

