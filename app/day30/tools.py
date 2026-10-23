
def calculator(operation, a, b):
    """Perform a basic mathematical operation."""

    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise ValueError("a must be a number")

    if not isinstance(b, (int, float)) or isinstance(b, bool):
        raise ValueError("b must be a number")

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
    else:
        raise ValueError("Unsupported operation")

    return {"result": result}


def knowledge_search(query):
    """Search a small knowledge base."""

    knowledge_base = {
        "redis": (
            "Redis is an in-memory data store commonly used "
            "for caching, sessions, and fast data access."
        ),
        "rabbitmq": (
            "RabbitMQ is a message broker that supports "
            "asynchronous communication between services."
        ),
        "spring boot": (
            "Spring Boot simplifies Java application development "
            "with auto-configuration and production-ready features."
        ),
        "rag": (
            "RAG retrieves relevant information from a knowledge "
            "source and provides it to an LLM for answering."
        ),
    }

    query_lower = query.lower()

    for topic, answer in knowledge_base.items():
        if topic in query_lower:
            return {"result": answer}

    return {
        "result": "No relevant information found.",
        "found": False
    }


def execute_tool(name, arguments):
    """Dispatch the requested tool safely."""

    try:
        if name == "calculator":
            result = calculator(**arguments)

        elif name == "knowledge_search":
            result = knowledge_search(**arguments)

        else:
            return {
                "ok": False,
                "error": f"Unknown tool: {name}"
            }

        return {"ok": True, "data": result}

    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return {
            "ok": False,
            "error": str(exc)
        }

    except Exception:
        return {
            "ok": False,
            "error": "Unexpected tool execution failure"
        }
