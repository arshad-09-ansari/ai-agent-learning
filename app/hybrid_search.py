import os
import math
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from google import genai

load_dotenv()

# -----------------------------
# Gemini Client
# -----------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"


# -----------------------------
# Documents
# -----------------------------

documents = [
    {
        "id": "doc_1",
        "text": """
        Redis is an in-memory data store commonly used for caching.
        Redis TTL defines how long a key remains available before it expires.
        Caching can reduce database load and improve application response time.
        """,
        "source": "redis.md",
        "category": "database"
    },

    {
        "id": "doc_2",
        "text": """
        JWT is a token-based authentication mechanism.
        A JWT contains information about the user and is usually sent with API requests.
        JWT expiration defines how long the authentication token remains valid.
        """,
        "source": "jwt.md",
        "category": "security"
    },

    {
        "id": "doc_3",
        "text": """
        SVC-57 is a Not_Found error returned when the requested resource does not exist.
        The API should return an HTTP 404 response when SVC-57 occurs.
        """,
        "source": "api-errors.md",
        "category": "api"
    },

    {
        "id": "doc_4",
        "text": """
        Spring Security provides authentication and authorization functionality
        for Spring Boot applications. JWT authentication can be implemented
        using filters in Spring Security.
        """,
        "source": "spring-security.md",
        "category": "security"
    },

    {
        "id": "doc_5",
        "text": """
        PostgreSQL indexes improve query performance by allowing the database
        to locate rows efficiently. Indexes should be created on columns
        frequently used in WHERE clauses.
        """,
        "source": "postgresql.md",
        "category": "database"
    },

    {
        "id": "doc_6",
        "text": """
        Redis distributed locking can be used when multiple application instances
        need coordinated access to a shared resource. A lock should have an
        expiration time to avoid deadlocks.
        """,
        "source": "redis-lock.md",
        "category": "database"
    },

    {
        "id": "doc_7",
        "text": """
        Payment services should validate webhook signatures before processing
        payment events. Invalid signatures should be rejected to prevent
        unauthorized payment updates.
        """,
        "source": "payment-security.md",
        "category": "payment"
    },

    {
        "id": "doc_8",
        "text": """
        HTTP 401 indicates that authentication is required or the provided
        authentication credentials are invalid.
        HTTP 403 indicates that the user is authenticated but does not
        have permission to access the resource.
        """,
        "source": "http-status.md",
        "category": "api"
    },

    {
        "id": "doc_9",
        "text": """
        Kafka is a distributed event streaming platform commonly used
        for asynchronous communication between microservices.
        Kafka topics contain partitions that allow messages to be distributed.
        """,
        "source": "kafka.md",
        "category": "messaging"
    },

    {
        "id": "doc_10",
        "text": """
        RabbitMQ is a message broker commonly used for asynchronous communication.
        Queues store messages until consumers process them.
        """,
        "source": "rabbitmq.md",
        "category": "messaging"
    }
]


# ============================================================
# 1. Embedding
# ============================================================

def create_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


# ============================================================
# 2. Cosine Similarity
# ============================================================

def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


# ============================================================
# 3. Semantic Search
# ============================================================

def semantic_search(query, top_k=5):

    query_embedding = create_embedding(query)

    results = []

    for doc in documents:

        doc_embedding = create_embedding(
            doc["text"]
        )

        score = cosine_similarity(
            query_embedding,
            doc_embedding
        )

        results.append({
            "id": doc["id"],
            "score": score,
            "document": doc
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# 4. BM25 Search
# ============================================================

def bm25_search(query, top_k=5):

    tokenized_documents = [
        doc["text"].lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    results = []

    for index, score in enumerate(scores):

        results.append({
            "id": documents[index]["id"],
            "score": float(score),
            "document": documents[index]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# 5. Reciprocal Rank Fusion
# ============================================================

def reciprocal_rank_fusion(
        semantic_results,
        bm25_results,
        k=60
):

    fusion_scores = {}

    # Semantic ranking
    for rank, result in enumerate(
            semantic_results,
            start=1
    ):

        document_id = result["id"]

        score = 1 / (k + rank)

        fusion_scores[document_id] = (
            fusion_scores.get(document_id, 0)
            + score
        )

    # BM25 ranking
    for rank, result in enumerate(
            bm25_results,
            start=1
    ):

        document_id = result["id"]

        score = 1 / (k + rank)

        fusion_scores[document_id] = (
            fusion_scores.get(document_id, 0)
            + score
        )

    # Sort by RRF score
    ranked_documents = sorted(
        fusion_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_documents


# ============================================================
# 6. Hybrid Search
# ============================================================

def hybrid_search(query, top_k=3):

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    # -----------------------------
    # Semantic Retrieval
    # -----------------------------

    semantic_results = semantic_search(
        query,
        top_k=5
    )

    print("\n--- SEMANTIC SEARCH ---")

    for rank, result in enumerate(
            semantic_results,
            start=1
    ):

        print(
            f"{rank}. "
            f"{result['id']} "
            f"| score={result['score']:.4f}"
        )

    # -----------------------------
    # BM25 Retrieval
    # -----------------------------

    bm25_results = bm25_search(
        query,
        top_k=5
    )

    print("\n--- BM25 SEARCH ---")

    for rank, result in enumerate(
            bm25_results,
            start=1
    ):

        print(
            f"{rank}. "
            f"{result['id']} "
            f"| score={result['score']:.4f}"
        )

    # -----------------------------
    # RRF
    # -----------------------------

    fused_results = reciprocal_rank_fusion(
        semantic_results,
        bm25_results
    )

    print("\n--- HYBRID / RRF RESULTS ---")

    final_results = []

    for rank, (document_id, rrf_score) in enumerate(
            fused_results[:top_k],
            start=1
    ):

        document = next(
            doc for doc in documents
            if doc["id"] == document_id
        )

        result = {
            "rank": rank,
            "id": document_id,
            "rrf_score": rrf_score,
            "document": document
        }

        final_results.append(result)

        print(
            f"\n{rank}. {document_id}"
        )

        print(
            f"RRF Score: {rrf_score:.6f}"
        )

        print(
            f"Source: {document['source']}"
        )

        print(
            f"Category: {document['category']}"
        )

        print(
            f"Text: {document['text'].strip()}"
        )

    return final_results


# ============================================================
# 7. Main
# ============================================================

if __name__ == "__main__":

    query = input(
        "\nEnter your question: "
    ).strip()

    hybrid_search(
        query,
        top_k=3
    )