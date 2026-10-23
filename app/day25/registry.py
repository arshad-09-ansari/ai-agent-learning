# Registry ek central dictionary maintain karegi. Har tool ke saath uska function aur expected arguments ki type information register hogi.

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    function: Callable[..., Any]
    argument_types: dict[str, type]
    required_args: tuple[str, ...]


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        tool = self._tools.get(name)

        if tool is None:
            raise KeyError(f"Unknown tool: {name}")

        return tool

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "arguments": list(tool.argument_types.keys()),
                "required": list(tool.required_args)
            }
            for tool in self._tools.values()
        ]
        
        
        
#  Registry kyun chahiye?
# Suppose tumhare paas 50 tools hain:
# - search_knowledge
# - multiply
# - create_ticket
# - get_order_status
# - query_database
# Agar tum har naye tool ko dispatcher ke andar hardcode karoge, toh code difficult to maintain ho jayega.
# Registry se tum tools register karte ho, aur dispatcher unhe naam se retrieve karta hai.