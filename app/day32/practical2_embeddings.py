from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.day32.config import API_KEY


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=API_KEY,
)

documents = [
    "Spring Boot uses dependency injection to manage objects.",
    "JWT tokens can protect REST API endpoints.",
    "Redis is used for caching frequently accessed data.",
    "Kafka supports asynchronous event-driven communication.",
]

# Step 1: Documents ko vectors mein convert karo
document_vectors = embeddings.embed_documents(documents)

# Step 2: User query ka vector banao
query = "How can I secure my backend APIs?"
query_vector = embeddings.embed_query(query)

# Step 3: Query aur document vectors ki similarity calculate karo
scores = cosine_similarity(
    [query_vector],
    document_vectors,
)[0]

# Step 4: Highest similarity pehle
ranked_results = sorted(
    zip(documents, scores),
    key=lambda item: item[1],
    reverse=True,
)

for document, score in ranked_results:
    print(f"Score: {score:.4f} | {document}")