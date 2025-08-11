from mem0 import Memory

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
        self.client = Memory.from_config(config) 

    def add_memory(self, messages, user_id):
        """Save a conversation session to memory"""

        return self.client.add(
            messages=messages,
            user_id=user_id
        )

    def search_memory(self, query, user_id):
        """Retrieve a memory based on query"""
        
        return self.client.search(
            query=query,
            user_id=user_id
        )

if __name__ == "__main__":
    client = MemoryClient()
    messages = [
        {
            "role": "user",
            "content": "I'm from Berlin"
        }   
    ]

    print("Added: ", client.add_memory(messages, "1"))
    print("Found: ", client.search_memory("Where am I from?", user_id="1"))