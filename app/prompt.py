from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterable

@dataclass
class Prompt:
    instructions: Optional[str] = None
    context: Optional[str] = None
    role: Optional[str] = None
    examples: Optional[str] = None
    output_format: Optional[str] = None
        
    _order: Iterable[str] = ('role', 'instructions', 'context', 'examples', 'output_format')

    def __str__(self) -> str:
        parts = []
        for attr in self._order:
            value = getattr(self, attr)
            parts.append(f"# {attr.upper()}\n{value}\n" )
        return "\n".join(parts)
        
MAIN_AGENT_PROMPT = Prompt(
    instructions="You are a helpful assistant.",
    context="You can answer questions, provide explanations, and assist with various tasks.",
    role="Your role is to assist the user in achieving their goals.",
    examples="For example, if the user asks about the weather, you can provide current weather information.",
    output_format="Please respond in a clear and concise manner.",
)

if __name__ == "__main__":
    print(MAIN_AGENT_PROMPT)