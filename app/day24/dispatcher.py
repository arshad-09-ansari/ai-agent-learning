# Dispatcher registry aur validator ko connect karta hai. Ye decide nahi karta ki user ka question kya hai; ye sirf requested tool ko safely execute karta hai.

import logging
from time import perf_counter
from tracemalloc import start

from app.day24.registry import get_tool
from app.day24.validator import validate_arguments


logger = logging.getLogger(__name__)


def dispatch(tool_name: str, arguments: dict) -> dict:
    start = perf_counter()

    tool = get_tool(tool_name)

    if tool is None:
        duration_ms = (perf_counter() - start) * 1000

        logger.warning(
            "tool=%s status=blocked duration_ms=%.2f",
            tool_name,
            duration_ms,
        )

        return {
            "ok": False,
            "error": f"Tool not allowed: {tool_name}",
        }

    try:
        validate_arguments(tool_name, arguments)

        result = tool(**arguments)

        duration_ms = (perf_counter() - start) * 1000

        logger.info(
            "tool=%s status=success duration_ms=%.2f",
            tool_name,
            duration_ms,
        )

        return {
            "ok": True,
            "tool": tool_name,
            "result": result,
            "duration_ms": round(duration_ms, 2),
        }

    except (ValueError, TypeError):
        duration_ms = (perf_counter() - start) * 1000

        logger.warning(
            "tool=%s status=failed duration_ms=%.2f",
            tool_name,
            duration_ms,
        )

        return {
            "ok": False,
            "tool": tool_name,
            "error": "Invalid arguments or tool operation failed.",
            "duration_ms": round(duration_ms, 2),
        }

    # except Exception:
    #     duration_ms = (perf_counter() - start) * 1000

    #     logger.error(
    #         "tool=%s status=error duration_ms=%.2f",
    #         tool_name,
    #         duration_ms,
    #     )

      
    except Exception:
     duration_ms = (perf_counter() - start) * 1000

    logger.exception(
        "tool=%s status=error duration_ms=%.2f",
        tool_name,
        duration_ms,
    )

    return {
        "ok": False,
        "tool": tool_name,
        "error": "Tool execution failed.",
        "duration_ms": round(duration_ms, 2),
         }

        # return {
        #     "ok": False,
        #     "tool": tool_name,
        #     "error": "Tool execution failed.",
        #     "duration_ms": round(duration_ms, 2),
        # }



# Behind the scenes: tool(**arguments) kya karta hai?
# suppose input hai 
# tool_name = "multiply"

# arguments = {
#     "a": 250,
#     "b": 4,
# }

# Registry se multiply function milega.
# then python main 

# multiply(**arguments) == multiply(a=250, b=4)