from logging import getLogger

from mem0 import Memory

from .message import Message


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

class MemoryClient:
    def __init__(self):
        self.memory = Memory.from_config(config)

    def add_memory(self, messages, user_id):
        """
        Save a conversation session to memory
        """

        return self.memory.add(
            messages=messages,
            user_id=user_id
        )

    def search_memory(self, query, user_id):
        """
        Retrieve a memory based on query
        """
        
        return self.memory.search(
            query=query,
            user_id=user_id
        )

if __name__ == "__main__":
    memory_client = MemoryClient()
    new = memory_client.add_memory(
        messages=[Message(content="I'm from Berline", role='user')],
        user_id='John'
    )
    print(f"Added: {new}")
    result = memory_client.search_memory("What's special about Berlin?", 'John')
    print(f"Found {result}")