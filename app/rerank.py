documents = [
    "Redis is an in-memory data store commonly used for caching.",
    "PostgreSQL is a relational database management system.",
    "Redis supports TTL which allows cached keys to expire automatically.",
    "Redis can be used for distributed locking.",
    "How does Redis improve application performance?",
    "Caching improves application performance by reducing database load."
]

query = "How can Redis automatically expire cached data?"


def simple_rerank(query, documents):
    query_words = set(query.lower().split())

    results = []

    for document in documents:
        document_words = set(document.lower().split())

        score = len(query_words.intersection(document_words))

        results.append((score, document))

    results.sort(reverse=True)

    return results


results = simple_rerank(query, documents)

for score, document in results:
    print(f"Score: {score}")
    print(document)
    print()