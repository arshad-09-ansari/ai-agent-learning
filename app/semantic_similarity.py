import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from google import genai
from app.config.settings import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=GEMINI_API_KEY)


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return result.embeddings[0].values


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = sum(a * a for a in vector_a) ** 0.5
    magnitude_b = sum(b * b for b in vector_b) ** 0.5

    return dot_product / (magnitude_a * magnitude_b)


text_a = "I want to learn Java"
text_b = "I want to study Java"
text_c = "The weather is very cold today"

vector_a = get_embedding(text_a)
vector_b = get_embedding(text_b)
vector_c = get_embedding(text_c)

similarity_ab = cosine_similarity(vector_a, vector_b)
similarity_ac = cosine_similarity(vector_a, vector_c)

print("\nText A:", text_a)
print("Text B:", text_b)
print("Text C:", text_c)

print("\nSimilarity A vs B:", similarity_ab)
print("Similarity A vs C:", similarity_ac)