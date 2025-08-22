from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterable

@dataclass
class Prompt:
    task: Optional[str] = None
    instructions: Optional[str] = None
    context: Optional[str] = None
    role: Optional[str] = None
    examples: Optional[str] = None
    output_format: Optional[str] = None
    data: Optional[str] = None
        
    _order: Iterable[str] = ('role', 'task', 'instructions', 'context', 'examples', 'output_format', 'data')

    def __str__(self) -> str:
        parts = []
        for attr in self._order:
            value = getattr(self, attr)
            parts.append(f"# {attr.upper()}\n{value}\n" )
        return "\n".join(parts)
    
    def parse_variables(self, **kwargs) -> str:
        prompt_str = str(self)
        for key, value in kwargs.items():
            prompt_str = prompt_str.replace(f"{{{key}}}", str(value))
        return prompt_str
        
MAIN_AGENT_PROMPT = Prompt(
    task="Your task is to assist the user with their queries and provide helpful responses.",
    instructions="You should use any tools necessary to complete the task.",
    context="You can answer questions, provide explanations, and assist with various tasks.",
    role="You are a helpful assistant.",
    examples="For example, if the user asks about the weather, you can provide current weather information.",
    output_format="Please respond in a clear and concise manner.",
    data="Here is the data: {data}"
)

if __name__ == "__main__":
    data = "WORKING"
    print(MAIN_AGENT_PROMPT.parse_variables(data=data))