import os

from mem0 import Memory
from agents import function_tool

from .message import Message
from .config import Mem0Config

cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "mem0.yaml")
mem0_cfg = Mem0Config()
memory_client = Memory.from_config(mem0_cfg)

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