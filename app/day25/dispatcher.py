import logging
import time
from typing import Any

from app.day25.registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolDispatcher:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any]
    ) -> dict[str, Any]:

        start = time.perf_counter()

        try:
            # 1. Validate the request structure
            if not isinstance(arguments, dict):
                raise ValueError(
                    "Tool arguments must be a dictionary"
                )

            # 2. Resolve only registered tools
            tool = self.registry.get(tool_name)

            # 3. Validate required arguments
            missing = [
                name
                for name in tool.required_args
                if name not in arguments
            ]

            if missing:
                raise ValueError(
                    f"Missing required arguments: {missing}"
                )

            # 4. Reject unexpected arguments
            allowed = set(tool.argument_types.keys())
            received = set(arguments.keys())

            unexpected = received - allowed

            if unexpected:
                raise ValueError(
                    f"Unexpected arguments: {sorted(unexpected)}"
                )

            # 5. Validate argument types
            for name, expected_type in tool.argument_types.items():
                if name not in arguments:
                    continue

                value = arguments[name]

                if expected_type is float:
                    valid = (
                        isinstance(value, (int, float))
                        and not isinstance(value, bool)
                    )
                else:
                    valid = isinstance(value, expected_type)

                if not valid:
                    raise ValueError(
                        f"Argument '{name}' must be "
                        f"{expected_type.__name__}"
                    )

            # 6. Execute the registered function
            result = tool.function(**arguments)

            duration_ms = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            logger.info(
                "tool=%s status=success duration_ms=%s",
                tool_name,
                duration_ms
            )

            return {
                "ok": True,
                "tool": tool_name,
                "result": result,
                "duration_ms": duration_ms
            }

        except (ValueError, KeyError) as exc:
            duration_ms = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            logger.warning(
                "tool=%s status=rejected duration_ms=%s reason=%s",
                tool_name,
                duration_ms,
                str(exc)
            )

            return {
                "ok": False,
                "tool": tool_name,
                "error": str(exc),
                "duration_ms": duration_ms
            }

        except Exception:
            duration_ms = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            logger.exception(
                "tool=%s status=error duration_ms=%s",
                tool_name,
                duration_ms
            )

            return {
                "ok": False,
                "tool": tool_name,
                "error": "Tool execution failed.",
                "duration_ms": duration_ms
            }