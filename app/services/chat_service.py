from app.llm.gemini_client import client
from app.config.settings import MODEL_NAME


def chat(prompt: str) -> str:
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents= prompt,
    )
    
    return response.text