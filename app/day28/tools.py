
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> dict[str, Any]:
    return {
        "ok": True,
        "result": a + b,
    }


def multiply(a: float, b: float) -> dict[str, Any]:
    return {
        "ok": True,
        "result": a * b,
    }


def subtract(a: float, b: float) -> dict[str, Any]:
    return {
        "ok": True,
        "result": a - b,
    }


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Execute an allowlisted tool with basic validation."""

    start = time.perf_counter()

    try:
        if not isinstance(arguments, dict):
            raise ValueError("Arguments must be a dictionary.")

        allowed_tools = {
            "add": add,
            "multiply": multiply,
            "subtract": subtract,
        }

        tool = allowed_tools.get(tool_name)

        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        a = arguments.get("a")
        b = arguments.get("b")

        # bool is a subclass of int in Python, so reject it explicitly.
        for value in (a, b):
            if isinstance(value, bool) or not isinstance(
                value, (int, float)
            ):
                raise ValueError("a and b must be numbers.")

            if not float("-inf") < value < float("inf"):
                raise ValueError("Numbers must be finite.")

        result = tool(a, b)

        logger.info(
            "tool=%s status=success duration_ms=%.2f",
            tool_name,
            (time.perf_counter() - start) * 1000,
        )

        return {
            "ok": True,
            "tool": tool_name,
            **result,
        }

    except (ValueError, TypeError) as exc:
        logger.warning(
            "tool=%s status=error error=%s",
            tool_name,
            str(exc),
        )

        return {
            "ok": False,
            "tool": tool_name,
            "error": str(exc),
        }

    except Exception:
        logger.exception("Unexpected tool execution error")

        return {
            "ok": False,
            "tool": tool_name,
            "error": "Internal tool execution error.",
        }
