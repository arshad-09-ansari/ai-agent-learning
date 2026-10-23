from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(query: str, context):

    prompt = f"""
You are a helpful company assistant.

Answer the user's question using the provided context.

If the context does not contain enough information,
clearly say that you don't have enough information.

Do not invent facts.

User Question:
{query}

Context:
{context}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text