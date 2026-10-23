
import math


def multiply(a: float, b: float) -> dict:
    """Multiply two finite numbers."""

    a = float(a)
    b = float(b)

    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Inputs must be finite numbers.")

    result = a * b

    if not math.isfinite(result):
        raise ValueError(
            "Result is outside the supported numeric range."
        )

    return {
        "ok": True,
        "result": result,
    }


def add(a: float, b: float) -> dict:
    """Add two finite numbers."""

    a = float(a)
    b = float(b)

    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Inputs must be finite numbers.")

    result = a + b

    if not math.isfinite(result):
        raise ValueError(
            "Result is outside the supported numeric range."
        )

    return {
        "ok": True,
        "result": result,
    }


def execute_tool(name: str, arguments: dict) -> dict:
    """Execute only approved tools."""

    allowed_tools = {
        "multiply": multiply,
        "add": add,
    }

    # 1. Validate tool name
    if name not in allowed_tools:
        return {
            "ok": False,
            "error": f"Tool '{name}' is not allowed.",
        }

    # 2. Validate arguments type
    if not isinstance(arguments, dict):
        return {
            "ok": False,
            "error": "Tool arguments must be an object.",
        }

    # 3. Validate argument names
    if set(arguments) != {"a", "b"}:
        return {
            "ok": False,
            "error": "Exactly two arguments, a and b, are required.",
        }

    # 4. Execute the selected tool
    try:
        result = allowed_tools[name](**arguments)
        return result

    except (TypeError, ValueError, OverflowError) as exc:
        return {
            "ok": False,
            "error": str(exc),
        }

    except Exception:
        return {
            "ok": False,
            "error": "Unexpected tool execution failure.",
        }
