from mem0 import Memory
from agents import function_tool

from .message import Message
from .config import Mem0Config


mem0_cfg = Mem0Config(_env_file = "test.env")

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 1024, 
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "gemma3:4b",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434", 
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "snowflake-arctic-embed2",
            "ollama_base_url": "http://localhost:11434",
        },
    },
}

memory_client = Memory(
    
)

# TODO: need a way to pass in user_id
@function_tool
def search_memory(query: str) -> str:
    """
    Retrieve a memory based on query
    Parameters:
      - query: free-text search string
    Returns:
      A dict with search matches.
    """
    return memory_client.search(query=query, user_id="John")

def add_mock_memory():
    print("Adding new memory")
    new = memory_client.add(
        messages=[Message(content='I want to cancel my insurance policy due to the high cost', role='user')],
        user_id='John',
    )
    print("Added: \n\n", new)

# Example Usage
if __name__ == "__main__":
    new = memory_client.add(
        messages=[Message(content='I want to cancel my insurance policy due to the high cost', role='user')],
        user_id='John',
    )
    print("Added: \n\n", new)

    result = memory_client.search(query="Why did I want to cancel my insurance", user_id='John')
    print(f"Found {result}")