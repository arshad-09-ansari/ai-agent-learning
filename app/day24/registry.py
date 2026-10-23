# Registry ek dictionary hai jo tool ke naam ko actual Python function se map karti hai.


from app.day24.tools import (
    add,
    multiply,
    subtract,
    knowledge_search,
)


TOOL_REGISTRY = {
    "add": add,
    "multiply": multiply,
     "subtract": subtract,
    "knowledge_search": knowledge_search,
}


def get_tool(tool_name: str):
    """Return an explicitly registered tool."""
    return TOOL_REGISTRY.get(tool_name)


def list_tools() -> list[str]:
    """Return the names of available tools."""
    return list(TOOL_REGISTRY.keys())


# from app.day24.registry import list_tools

# print(list_tools())