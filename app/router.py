def route_query(query: str):

    query_lower = query.lower()

    document_keywords = [
        "policy",
        "refund",
        "cancellation",
        "shipping",
        "security",
        "jwt",
        "authentication",
        "password",
        "customer data"
    ]

    product_keywords = [
        "price",
        "cost",
        "stock",
        "available",
        "product",
        "laptop",
        "headphones",
        "keyboard",
        "watch"
    ]

    if any(word in query_lower for word in document_keywords):
        return "documents"

    if any(word in query_lower for word in product_keywords):
        return "products"

    return "general"

if __name__ == "__main__":

    queries = [
        "What is the refund policy?",
        "What is the price of Laptop Pro?",
        "Is the keyboard available?",
        "What is JWT?",
        "Tell me a joke"
    ]

    for query in queries:

        route = route_query(query)

        print(f"Query: {query}")
        print(f"Route: {route}")
        print("-" * 40)