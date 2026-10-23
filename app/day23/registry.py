# app/day23/registry.py

from app.day23.tools import (
    add,
    multiply,
    search_knowledge_base,
)

TOOL_REGISTRY = {
    "add": add,
    "multiply": multiply,
    "search_knowledge_base": search_knowledge_base,
}