import json
import math
import os

from dotenv import load_dotenv
from google import genai
from rank_bm25 import BM25Okapi


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-embedding-001"


# ----------------------------------------
# Load stored documents
# ----------------------------------------

with open(
    "data/embeddings.json",
    "r",
    encoding="utf-8"
) as file:

    documents = json.load(file)


# ----------------------------------------
# Cosine similarity
# ----------------------------------------

def cosine_similarity(a, b):

    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(x * x for x in b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot / (
        magnitude_a * magnitude_b
    )


# ----------------------------------------
# Query embedding
# ----------------------------------------

def create_query_embedding(query):

    response = client.models.embed_content(
        model=MODEL,
        contents=query
    )

    return response.embeddings[0].values


# ----------------------------------------
# Metadata filtering
# ----------------------------------------

def filter_documents(
        documents,
        category=None
):

    if category is None:
        return documents

    return [
        doc
        for doc in documents
        if doc["category"] == category
    ]


# ----------------------------------------
# Vector Search
# ----------------------------------------

def vector_search(
        query,
        documents,
        top_k=5
):

    query_embedding = create_query_embedding(
        query
    )

    results = []

    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )

        results.append({
            "id": document["id"],
            "score": score,
            "document": document
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ----------------------------------------
# BM25 Search
# ----------------------------------------

def bm25_search(
        query,
        documents,
        top_k=5
):

    tokenized_documents = [
        doc["text"].lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    query_tokens = query.lower().split()

    scores = bm25.get_scores(
        query_tokens
    )

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


# ----------------------------------------
# RRF
# ----------------------------------------

def rrf(
        vector_results,
        bm25_results,
        k=60
):

    scores = {}

    for rank, result in enumerate(
            vector_results,
            start=1
    ):

        doc_id = result["id"]

        scores[doc_id] = (
            scores.get(doc_id, 0)
            + 1 / (k + rank)
        )

    for rank, result in enumerate(
            bm25_results,
            start=1
    ):

        doc_id = result["id"]

        scores[doc_id] = (
            scores.get(doc_id, 0)
            + 1 / (k + rank)
        )

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


# ----------------------------------------
# Production Retrieval
# ----------------------------------------

def retrieve(
        query,
        category=None,
        top_k=3
):

    print("\n================================")
    print("QUERY:", query)
    print("CATEGORY:", category)
    print("================================")

    # 1. Metadata filtering

    filtered_documents = filter_documents(
        documents,
        category
    )

    print(
        "\nDocuments after filtering:",
        len(filtered_documents)
    )

    # 2. Vector retrieval

    vector_results = vector_search(
        query,
        filtered_documents,
        top_k=5
    )

    # 3. BM25 retrieval

    bm25_results = bm25_search(
        query,
        filtered_documents,
        top_k=5
    )

    # 4. Fusion

    fused_results = rrf(
        vector_results,
        bm25_results
    )

    print("\nFINAL HYBRID RESULTS:")

    final_results = []

    for rank, (doc_id, score) in enumerate(
            fused_results[:top_k],
            start=1
    ):

        document = next(
            doc
            for doc in filtered_documents
            if doc["id"] == doc_id
        )

        result = {
            "rank": rank,
            "id": doc_id,
            "score": score,
            "source": document["source"],
            "category": document["category"],
            "text": document["text"]
        }

        final_results.append(result)

        print(
            f"\n{rank}. {doc_id}"
        )

        print(
            f"RRF: {score:.6f}"
        )

        print(
            f"Source: {document['source']}"
        )

        print(
            f"Category: {document['category']}"
        )

        print(
            f"Text: {document['text']}"
        )

    return final_results


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    query = input(
        "\nEnter query: "
    ).strip()

    category = input(
        "Category filter "
        "(api/security/database/payment/messaging/blank): "
    ).strip()

    if category == "":
        category = None

    retrieve(
        query=query,
        category=category,
        top_k=3
    )