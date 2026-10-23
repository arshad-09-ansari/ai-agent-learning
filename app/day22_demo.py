from router import route_query


queries = [
    "What is our refund policy?",
    "What is the current balance of customer 1024?",
    "What happened with order 12345?",
    "What is the weather today?",
    "How does authentication work?"
]


for query in queries:

    route = route_query(query)

    print(f"\nQuery: {query}")
    print(f"Route: {route}")