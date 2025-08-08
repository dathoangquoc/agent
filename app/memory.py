from mem0 import Memory

class Memory:
    def __init__(self):
        self.memo = Memory()

    """Add memory whenever your agent learns something useful:
A new user preference is shared
A decision or suggestion is made
A goal or task is completed
A new entity is introduced
A user gives feedback or clarification
    """    

    def add_memory(self, messages):
        query = ""
        self.mem0.search(
            query=query,
            user_id=""
        )

    def search_memory(self, query):
        self.mem0.search(
            query=query,
            user_id=""
        )