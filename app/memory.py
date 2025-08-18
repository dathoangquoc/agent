import os

from mem0 import Memory
from agents import function_tool
from yaml import safe_load

from .message import Message
from .config import Mem0Config


with open("./config/mem0.test.yaml", "r") as f:
    mem0_cfg = safe_load(f)
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

@function_tool
def add_memory(messages: list[Message]) -> str:
    """
    Add a new memory to the memory store
    Parameters:
      - messages: list of messages to add
    Returns:
      A dict with the added memory.
    """
    return memory_client.add(messages=messages, user_id="John")

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