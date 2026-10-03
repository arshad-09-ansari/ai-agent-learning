from google import genai

from app.config.settings import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file or environment variables."
    )

client = genai.Client(api_key=GEMINI_API_KEY)