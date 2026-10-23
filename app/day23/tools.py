
# app/day23/tools.py

DOCUMENTS = {
    "java": (
        "Java is a strongly typed, object-oriented "
        "programming language that runs on the JVM."
    ),
    "spring boot": (
        "Spring Boot simplifies Spring application development "
        "using auto-configuration, starters, and embedded servers."
    ),
    "redis": (
        "Redis is an in-memory data store commonly used for "
        "caching, counters, sessions, and low-latency data access."
    ),
    "kafka": (
        "Apache Kafka is a distributed event-streaming platform "
        "used to publish, store, and consume event streams."
    ),
}


def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def search_knowledge_base(query: str) -> dict:
    """Search a small local technical knowledge base."""

    query = query.strip().lower()

    if not query:
        return {
            "found": False,
            "results": [],
            "message": "Query cannot be empty."
        }

    matches = []

    for topic, content in DOCUMENTS.items():
        if topic in query or query in topic:
            matches.append({
                "topic": topic,
                "content": content
            })

    return {
        "found": bool(matches),
        "results": matches,
        "message": (
            "Results found." if matches
            else "No matching document found."
        )
    }
