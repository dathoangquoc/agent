from mem0 import Memory
from agents import function_tool
from yaml import safe_load


with open("./config/mem0.prod.yml", "r") as f:
    mem0_cfg = safe_load(f)
    memory_client = Memory.from_config(mem0_cfg)

def create_memory_tools(chat_instance):
  """
  Create memory tools for the agent
  """

  @function_tool
  def search_memory(query: str) -> str:
      """
      Retrieve a memory about the user based on a query
      Parameters:
        - query: free-text search string
      Returns:
        A dict with search matches.
      """
      # print(f"Searching memory for query: {query}")
      found = memory_client.search(query=query, user_id=chat_instance.user_id)
      # print(f"Found: {found}")
      return found

  @function_tool
  def add_memory() -> str:
      """
      Add the current conversation to the memory store whenever you learns something useful:
      - A new user preference is shared
      - A decision or suggestion is made
      - A goal or task is completed
      - A new entity is introduced
      - A user gives feedback or clarification

      Parameters:
        - messages: list of messages to add
      Returns:
        A dict with the added memory.
      """
      # print(f"Adding: {chat_instance.history} to memory for user [{chat_instance.user_id}]")
      messages = chat_instance.history
      if not messages:
          return "No messages to add to memory."
      found = memory_client.add(messages=messages, user_id=chat_instance.user_id, run_id=chat_instance.session_id)
      # Clear the messages after adding to memory to prevent the same messages from being added again next time
      chat_instance.history = []

      # print(f"Added to memory: {found}")
      return found
  
  def get_last_session(query) -> str:
      """
      Get the last session of the user
      Returns:
        A dict with the last session memory.
      """
      # print(f"Getting last session for user [{chat_instance.user_id}]")
      last_session = memory_client.search(query=query, user_id=chat_instance.user_id, run_id=chat_instance.session_id)
      # print(f"Last session: {last_session}")
      return last_session

  return search_memory, add_memory, get_last_session