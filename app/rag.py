import sys
from pathlib import Path

# Allow running:
# python app/rag.py
if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[1]

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


from google import genai
from sklearn.metrics.pairwise import cosine_similarity

from app.config.settings import GEMINI_API_KEY, MODEL_NAME


# --------------------------------
# 1. Check environment
# --------------------------------

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )

print("API key loaded:", bool(GEMINI_API_KEY))
print("Model:", MODEL_NAME)


# --------------------------------
# 2. Create Gemini client
# --------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------
# 3. Create embedding
# --------------------------------

def create_embedding(text: str):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values


# --------------------------------
# 4. RAG pipeline
# --------------------------------

def run_rag(query: str, top_k: int = 3):

    # Knowledge base
    documents = [
        "Java is a popular object-oriented programming language.",
        "Spring Boot is a Java framework used to build production-ready backend applications.",
        "Redis is an in-memory data store commonly used for caching.",
        "PostgreSQL is a relational database management system.",
        "Apache Kafka is a distributed event streaming platform.",
        "Docker is used to package applications and their dependencies into containers.",
        "Kubernetes is used to orchestrate containerized applications.",
        "React is a JavaScript library commonly used to build user interfaces."
    ]

    # --------------------------------
    # Step 1: Embed documents
    # --------------------------------

    document_embeddings = [
        create_embedding(document)
        for document in documents
    ]

    # --------------------------------
    # Step 2: Embed user query
    # --------------------------------

    query_embedding = create_embedding(query)

    # --------------------------------
    # Step 3: Calculate similarity
    # --------------------------------

    similarities = cosine_similarity(
        [query_embedding],
        document_embeddings
    )[0]

    # --------------------------------
    # Step 4: Get Top-K documents
    # --------------------------------

    top_indices = similarities.argsort()[::-1][:top_k]

    # --------------------------------
    # Step 5: Build context
    # --------------------------------

    context = "\n".join(
        documents[index]
        for index in top_indices
    )

    # --------------------------------
    # Step 6: Create RAG prompt
    # --------------------------------

    prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{query}

If the answer is not available in the context,
say "I don't have enough information."
"""

    # --------------------------------
    # Step 7: Generate answer
    # --------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    # --------------------------------
    # Step 8: Return result
    # --------------------------------

    return {
        "query": query,
        "context": context,
        "answer": response.text
    }


# --------------------------------
# 5. Run application
# --------------------------------

if __name__ == "__main__":

    query = "What technologies are commonly used in backend development?"

    result = run_rag(query, top_k=5)

    print("\nQuestion:")
    print(result["query"])

    print("\nRetrieved Context:")
    print(result["context"])

    print("\nFinal Answer:")
    print(result["answer"])