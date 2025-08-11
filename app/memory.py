from mem0 import Memory
from agents import function_tool
from message import Message


config = config = {
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

memory = Memory.from_config(config)

def add_memory(messages, user_id):
    """Save a conversation session to memory"""

    return memory.add(
        messages=messages,
        user_id=user_id
    )

# @function_tool
def search_memory(query, user_id):
    """Retrieve a memory based on query"""
    return memory.search(
        query=query,
        user_id=user_id
    )

if __name__ == "__main__":
    new = add_memory(
        messages=[Message(content="I'm from Berline", role='user')],
        user_id='John'
    )
    print(f"Added: {new}")
    result = search_memory("What's special about Berlin?", 'John')
    print(f"Found {result}")