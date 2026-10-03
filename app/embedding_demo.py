import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

try:
    from google import genai
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependency 'google-genai'. Run: .\\venv\\Scripts\\python -m pip install -r requirements.txt"
    ) from exc

from app.config.settings import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file or environment variables."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

texts = [
    "I want to learn Java",
    "I want to study Java",
    "The weather is very cold today",
]

for text in texts:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    vector = result.embeddings[0].values

    print("\nText:", text)
    print("Vector dimensions:", len(vector))
    print("First 5 values:", vector[:5])