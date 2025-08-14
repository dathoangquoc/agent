from mem0 import Memory
from agents import function_tool

from .message import Message


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
            "model": "qwen3:4b",
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

memory_client = Memory.from_config(config)

# TODO: need a way to pass in user_id
@function_tool
def search_memory(query: str, user_id: str) -> str:
    """
    Retrieve a memory based on query and user_id.
    Parameters:
      - query: free-text search string
      - user_id: who to search memories for
    Returns:
      A dict with search matches.
    """
    return memory_client.search(query=query, user_id=user_id)

# Example Usage
if __name__ == "__main__":
    new = memory_client.add(
        messages=[Message(content="I'm from Berlin", role='user')],
        user_id='John'
    )
    print(f"Added: {new}")
    result = memory_client.search(query="What's special about Berlin?", user_id='John')
    print(f"Found {result}")