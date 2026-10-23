
import logging
from time import perf_counter

logger = logging.getLogger(__name__)


def multiply(a, b):
    """Multiply two finite numbers."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not allowed.")

    if not isinstance(a, (int, float)):
        raise ValueError("a must be a number.")

    if not isinstance(b, (int, float)):
        raise ValueError("b must be a number.")

    result = a * b

    if isinstance(result, float):
        if not __import__("math").isfinite(result):
            raise ValueError("Result must be finite.")

    return result


def knowledge_search(query):
    """Search a small local knowledge base."""
    documents = {
        "redis": (
            "Redis is an in-memory data store commonly used "
            "for caching, sessions, queues and fast lookups."
        ),
        "spring boot": (
            "Spring Boot simplifies Java application development "
            "using auto-configuration and starter dependencies."
        ),
        "rag": (
            "RAG retrieves relevant information from a knowledge "
            "source and provides it to an LLM as context."
        ),
        "agent": (
            "An AI agent uses an LLM to select actions, execute "
            "tools, observe results and decide what to do next."
        ),
    }

    query = query.strip().lower()

    if not query:
        raise ValueError("Query cannot be empty.")

    matches = [
        {"topic": topic, "content": content}
        for topic, content in documents.items()
        if topic in query or query in topic
    ]

    if not matches:
        return {
            "message": "No matching local document found.",
            "available_topics": list(documents.keys()),
        }

    return {"results": matches}


TOOLS = {
    "multiply": multiply,
    "knowledge_search": knowledge_search,
}


def execute_tool(name, arguments):
    """Execute an allowlisted tool and return a safe result."""
    start = perf_counter()

    try:
        if name not in TOOLS:
            raise ValueError(f"Unknown tool: {name}")

        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be an object.")

        function = TOOLS[name]
        result = function(**arguments)

        logger.info(
            "tool=%s status=success duration_ms=%.2f",
            name,
            (perf_counter() - start) * 1000,
        )

        return {
            "ok": True,
            "tool": name,
            "result": result,
        }

    except Exception as exc:
        logger.exception("Tool execution failed: %s", name)

        return {
            "ok": False,
            "tool": name,
            "error": str(exc),
        }
