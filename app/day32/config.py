import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

sampling_options = (
    {}
    if MODEL_NAME.lower() in {"gemini-3.6-flash", "gemini-3.5-flash-lite"}
    else {"temperature": 0.2}
)

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=API_KEY,
    max_retries=2,
    timeout=60,
    **sampling_options,
)