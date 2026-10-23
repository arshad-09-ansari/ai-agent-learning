
# app/day23/executor.py

import logging
from app.day23.registry import TOOL_REGISTRY

logger = logging.getLogger(__name__)

# Explicit argument allowlist for each tool.
ALLOWED_ARGUMENTS = {
    "add": {"a", "b"},
    "multiply": {"a", "b"},
    "search_knowledge_base": {"query"},
}


def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Validate and execute one registered tool."""

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Arguments must be an object."
        }

    allowed = ALLOWED_ARGUMENTS[tool_name]

    # Reject unexpected parameters.
    if set(arguments) - allowed:
        return {
            "success": False,
            "error": "Unexpected tool arguments."
        }

    # Require all expected parameters.
    if set(arguments) != allowed:
        return {
            "success": False,
            "error": "Missing required tool arguments."
        }

    # Validate actual argument types.
    if tool_name in {"add", "multiply"}:
        a = arguments["a"]
        b = arguments["b"]

        # bool is a subclass of int in Python.
        if (
            type(a) is not int
            or type(b) is not int
        ):
            return {
                "success": False,
                "error": "Both a and b must be integers."
            }

    elif tool_name == "search_knowledge_base":
        if not isinstance(arguments["query"], str):
            return {
                "success": False,
                "error": "query must be a string."
            }

    try:
        tool = TOOL_REGISTRY[tool_name]
        result = tool(**arguments)

        logger.info("Tool %s executed successfully", tool_name)

        return {
            "success": True,
            "data": result
        }

    except Exception:
        # Keep internal exception details in server logs.
        logger.exception("Tool %s failed", tool_name)

        return {
            "success": False,
            "error": "Tool execution failed."
        }
