from google import genai
from dotenv import load_dotenv
import os
import json
import math
from pathlib import Path

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
DATA_DIR = Path(__file__).resolve().parent / "data"


# -----------------------------
# 1. Cosine Similarity
# -----------------------------

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


# -----------------------------
# 2. Load Vector Store
# -----------------------------

vector_store_path = DATA_DIR / "vector_store.json"

if not vector_store_path.is_file():
    raise FileNotFoundError(
        f"Vector store not found at {vector_store_path}. "
        "Run `python app/ingest.py` first."
    )

if vector_store_path.stat().st_size == 0:
    raise ValueError(
        f"Vector store at {vector_store_path} is empty. "
        "Run `python app/ingest.py` first."
    )

with open(vector_store_path, "r", encoding="utf-8") as file:
    documents = json.load(file)


# -----------------------------
# 3. User Query
# -----------------------------

query = input("Ask a question: ")


# -----------------------------
# 4. Create Query Embedding
# -----------------------------

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_embedding = response.embeddings[0].values


# -----------------------------
# 5. Calculate Similarity
# -----------------------------

results = []

for document in documents:

    score = cosine_similarity(
        query_embedding,
        document["embedding"]
    )

    results.append({
        "text": document["text"],
        "score": score
    })


# -----------------------------
# 6. Sort by Similarity
# -----------------------------

results.sort(
    key=lambda x: x["score"],
    reverse=True
)


# -----------------------------
# 7. Top-K
# -----------------------------

top_k = 3

print("\nTop results:\n")

for result in results[:top_k]:

    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print("-" * 50)