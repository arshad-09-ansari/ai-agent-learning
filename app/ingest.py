from google import genai
from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DATA_DIR = Path(__file__).resolve().parent / "data"

# Read documents
with open(DATA_DIR / "knowledge.txt", "r", encoding="utf-8") as file:
    documents = file.readlines()

vectors = []

for document in documents:
    document = document.strip()

    if not document:
        continue

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=document
    )

    embedding = response.embeddings[0].values

    vectors.append({
        "text": document,
        "embedding": embedding
    })

# Save vectors
with open(DATA_DIR / "vector_store.json", "w", encoding="utf-8") as file:
    json.dump(vectors, file)

print(f"Stored {len(vectors)} documents.")