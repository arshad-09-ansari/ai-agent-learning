from google import genai
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

documents = [
    "Java is a popular programming language.",
    "Spring Boot is used to build Java backend applications.",
    "Python is widely used for artificial intelligence.",
    "You can learn Java through projects and regular practice.",
    "The weather is very cold today."
]

query = "How can I study Java?"

def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values


query_embedding = get_embedding(query)

document_embeddings = [
    get_embedding(document)
    for document in documents
]

scores = cosine_similarity(
    [query_embedding],
    document_embeddings
)[0]

results = list(zip(documents, scores))

results.sort(key=lambda x: x[1], reverse=True)

print("\nQuery:")
print(query)

print("\nSemantic Search Results:")

for document, score in results:
    print(f"{score:.4f} -> {document}")