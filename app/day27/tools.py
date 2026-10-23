
import logging
import time

logger = logging.getLogger(__name__)


def multiply(a: float, b: float) -> dict:
    """Multiply two finite numbers."""
    return {
        "ok": True,
        "result": a * b
    }


def add(a: float, b: float) -> dict:
    """Add two finite numbers."""
    return {
        "ok": True,
        "result": a + b
    }


def knowledge_search(query: str) -> dict:
    """
    Search the existing Day 26 knowledge tool.
    Adapt the imported function if your project uses a different name.
    """
    from app.day26.tools import execute_tool as day26_execute_tool

    return day26_execute_tool(
        "knowledge_search",
        {"query": query}
    )


TOOL_REGISTRY = {
    "multiply": multiply,
    "add": add,
    "knowledge_search": knowledge_search,
}


def execute_tool(name: str, arguments: dict) -> dict:
    start = time.perf_counter()

    try:
        if name not in TOOL_REGISTRY:
            return {
                "ok": False,
                "tool": name,
                "error": "Unknown tool."
            }

        if not isinstance(arguments, dict):
            return {
                "ok": False,
                "tool": name,
                "error": "Arguments must be an object."
            }

        if name in ("multiply", "add"):
            if set(arguments) != {"a", "b"}:
                return {
                    "ok": False,
                    "tool": name,
                    "error": "Expected exactly a and b."
                }

            for key in ("a", "b"):
                value = arguments[key]

                # bool is a subclass of int in Python.
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                ):
                    return {
                        "ok": False,
                        "tool": name,
                        "error": f"{key} must be a number."
                    }

                if not float("-inf") < value < float("inf"):
                    return {
                        "ok": False,
                        "tool": name,
                        "error": f"{key} must be finite."
                    }

        if name == "knowledge_search":
            if set(arguments) != {"query"}:
                return {
                    "ok": False,
                    "tool": name,
                    "error": "Expected exactly query."
                }

            query = arguments["query"]

            if not isinstance(query, str) or not query.strip():
                return {
                    "ok": False,
                    "tool": name,
                    "error": "Query must be a non-empty string."
                }

        result = TOOL_REGISTRY[name](**arguments)

        if not isinstance(result, dict):
            result = {"ok": True, "result": result}

        return {
            **result,
            "tool": name,
            "duration_ms": round(
                (time.perf_counter() - start) * 1000, 2
            )
        }

    except Exception:
        logger.exception("Tool execution failed: %s", name)

        return {
            "ok": False,
            "tool": name,
            "error": "Tool execution failed.",
            "duration_ms": round(
                (time.perf_counter() - start) * 1000, 2
            )
        }
