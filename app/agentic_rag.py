from router import route_query
from product_db import search_products
import document_retriever


def agentic_retrieve(query: str):

    route = route_query(query)

    print(f"\n[Router] Selected route: {route}")

    if route == "documents":

        results = document_retriever.retrieve_documents(query)

        return {
            "route": route,
            "context": results
        }

    elif route == "products":

        results = search_products(query)

        return {
            "route": route,
            "context": results
        }

    else:

        return {
            "route": route,
            "context": []
        }


if __name__ == "__main__":

    queries = [
        "What is the refund policy?",
        "What is the price of Laptop Pro?",
        "Is the Smart Watch available?",
        "What is JWT authentication?"
    ]

    for query in queries:

        print("\n" + "=" * 60)
        print("USER:", query)

        result = agentic_retrieve(query)

        print("ROUTE:", result["route"])
        print("CONTEXT:", result["context"])