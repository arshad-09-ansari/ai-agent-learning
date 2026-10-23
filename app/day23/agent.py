import logging
import os

from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError as exc:  # pragma: no cover - dependency check at import time
    raise RuntimeError(
        "google-genai is required. Install it with `pip install google-genai`."
    ) from exc

from app.day23.executor import execute_tool

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-prototype-1")

if not API_KEY:
    logger.error("API_KEY is not set in the environment.")
    raise ValueError("API_KEY is required.")
if not MODEL_NAME:
    logger.error("MODEL_NAME is not set in the environment.")
    raise ValueError("MODEL_NAME is required.")

client = genai.Client(api_key=API_KEY)

TOOL = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="multiply",
                description="Multiply two integers.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "a": types.Schema(
                            type=types.Type.INTEGER,
                            description="The first integer to multiply.",
                        ),
                        "b": types.Schema(
                            type=types.Type.INTEGER,
                            description="The second integer to multiply.",
                        ),
                    },
                    required=["a", "b"],
                ),
            ),
            types.FunctionDeclaration(
                name="add",
                description="Add two integers.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "a": types.Schema(
                            type=types.Type.INTEGER,
                            description="The first integer to add.",
                        ),
                        "b": types.Schema(
                            type=types.Type.INTEGER,
                            description="The second integer to add.",
                        ),
                    },
                    required=["a", "b"],
                ),
            ),
            types.FunctionDeclaration(
                name="search_knowledge_base",
                description=(
                    "Search the local technical knowledge base for Java, Spring Boot, "
                    "Redis or Kafka."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="Topic to search for.",
                        )
                    },
                    required=["query"],
                ),
            ),
        ]
    )
]

__all__ = ["API_KEY", "MODEL_NAME", "TOOL", "client", "execute_tool"]
