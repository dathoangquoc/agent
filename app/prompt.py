class Prompt:
    def __init__(self, system, role, instruction):
        self.system = system
        self.role = role
        self.instruction = instruction

MAIN_AGENT_PROMPT = """
You are a 
"""