
import os
import json
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.day27.tools import execute_tool

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

MAX_STEPS = 5

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="multiply",
        description="Multiply two numbers.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {"type": "NUMBER"},
                "b": {"type": "NUMBER"}
            },
            "required": ["a", "b"]
        }
    ),
    types.FunctionDeclaration(
        name="add",
        description="Add two numbers.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {"type": "NUMBER"},
                "b": {"type": "NUMBER"}
            },
            "required": ["a", "b"]
        }
    ),
    types.FunctionDeclaration(
        name="knowledge_search",
        description=(
            "Search the local technical knowledge base "
            "for information about Java, Redis, RAG, etc."
        ),
        parameters={
            "type": "OBJECT",
            "properties": {
                "query": {"type": "STRING"}
            },
            "required": ["query"]
        }
    )
]

TOOLS = [
    types.Tool(function_declarations=TOOL_DECLARATIONS)
]


def run_agent(user_query: str) -> str:
    if not user_query.strip():
        return "Please enter a question."

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)]
        )
    ]

    for step in range(1, MAX_STEPS + 1):
        logging.info("Agent step %s", step)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=TOOLS,
                temperature=0
            )
        )

        if not response.candidates:
            return "The model returned no candidates."

        model_content = response.candidates[0].content
        if model_content is None:
            return "The model returned an empty response."

        # Preserve the model response in conversation history.
        contents.append(model_content)

        function_calls = [
            part.function_call
            for part in (model_content.parts or [])
            if part.function_call is not None
        ]

        # No tool request means the model has finished.
        if not function_calls:
            return response.text or "No final text was returned."

        # Execute requested tools and send their results together.
        function_response_parts = []

        for call in function_calls:
            name = call.name
            arguments = dict(call.args or {})

            logging.info(
                "Tool call: %s | arguments: %s",
                name,
                arguments
            )

            result = execute_tool(name, arguments)

            logging.info(
                "Tool result: %s | success: %s",
                name,
                result.get("ok", False)
            )

            function_response_parts.append(
                types.Part.from_function_response(
                    name=name,
                    response={
                        "result": json.dumps(
                            result,
                            default=str
                        )
                    }
                )
            )

        contents.append(
            types.Content(
                role="tool",
                parts=function_response_parts
            )
        )

    return (
        f"Stopped: maximum of {MAX_STEPS} agent steps reached."
    )


if __name__ == "__main__":
    while True:
        query = input("\nYou: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Agent stopped.")
            break

        try:
            answer = run_agent(query)
            print("\nAgent:", answer)

        except Exception:
            logging.exception("Agent request failed")
            print(
                "Agent error. Check the traceback and API configuration."
            )
