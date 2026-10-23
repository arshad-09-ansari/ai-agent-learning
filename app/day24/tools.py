# Tool ka matlab hai ek normal Python function jise agent kisi specific task ke liye use kar sakta hai.
from app.production_retrieve import retrieve
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b



def knowledge_search(query: str) -> dict:
    """Search the existing RAG retrieval pipeline."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    results = retrieve(
        query=query,
        category=None,
        top_k=3,
    )

    if not results:
        return {
            "query": query,
            "found": False,
            "results": [],
        }

    return {
        "query": query,
        "found": True,
        "results": results,
    }



# Code ko samjho
# - add() aur multiply() deterministic functions hain: same input par same output milega.
# - knowledge_search() ek local demo knowledge base search karta hai.
# - dict return karne se result ko structured format mein agent tak bhejna easy hota hai.
# - Ye actual vector search nahi hai. Production mein tum is function ko apne existing retrieve.py ya hybrid-search pipeline se connect karoge.