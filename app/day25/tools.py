def add(a: float, b: float) -> float:
    return a + b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


def search_knowledge(query: str) -> dict:
    documents = {
        "redis": "Redis is an in-memory data store.",
        "spring boot": "Spring Boot simplifies Java application development.",
        "rag": "RAG retrieves relevant information before generating an answer."
    }

    query_lower = query.lower()

    for topic, content in documents.items():
        if topic in query_lower:
            return {
                "found": True,
                "topic": topic,
                "content": content
            }

    return {
        "found": False,
        "topic": None,
        "content": "No matching document found."
    }
    
    
    
#     Code ka internal working
# - add() aur multiply() deterministic calculations karte hain.
# - divide() invalid input par controlled exception raise karta hai.
# - search_knowledge() ek basic local knowledge search hai. Ye tumhare Day 19 hybrid search ya Day 22 routing ka replacement nahi hai; abhi hum tool execution ka mechanism seekh rahe hain.
# Production mein tools APIs, databases, RAG pipelines aur approved business operations ko call kar sakte hain.