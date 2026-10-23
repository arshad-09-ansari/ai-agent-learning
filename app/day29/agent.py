
import os
import json
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.day29.tools import execute_tool

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

tool_declarations = [
    types.FunctionDeclaration(
        name="multiply",
        description="Multiply two numbers.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {
                    "type": "NUMBER",
                    "description": "First number",
                },
                "b": {
                    "type": "NUMBER",
                    "description": "Second number",
                },
            },
            "required": ["a", "b"],
        },
    ),
    types.FunctionDeclaration(
        name="knowledge_search",
        description=(
            "Search local knowledge for topics such as "
            "Redis, Spring Boot, RAG and AI agents."
        ),
        parameters={
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Topic to search for",
                },
            },
            "required": ["query"],
        },
    ),
]

agent_tools = [
    types.Tool(function_declarations=tool_declarations)
]


def run_agent(user_query, max_steps=6):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)],
        )
    ]

    for step in range(1, max_steps + 1):
        logger.info("Agent step %s", step)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=agent_tools,
                system_instruction=(
                    "You are a helpful AI agent. "
                    "Use tools when needed. You may call multiple "
                    "tools over multiple turns. After receiving "
                    "tool results, decide whether another tool "
                    "is needed. Never claim a tool succeeded if "
                    "its result says ok=false. When enough "
                    "information is available, answer the user."
                ),
            ),
        )

        if not response.candidates:
            return "The model returned no candidate response."

        model_content = response.candidates[0].content
        contents.append(model_content)

        function_calls = [
            part.function_call
            for part in (model_content.parts or [])
            if part.function_call is not None
        ]

        # No tool calls means the model has finished.
        if not function_calls:
            return response.text or "No text response was returned."

        function_responses = []

        for function_call in function_calls:
            name = function_call.name
            arguments = dict(function_call.args or {})

            logger.info(
                "Executing tool=%s arguments=%s",
                name,
                json.dumps(arguments),
            )

            result = execute_tool(name, arguments)

            function_responses.append(
                types.Part.from_function_response(
                    name=name,
                    response=result,
                )
            )

        # Send every tool result back to the model.
        contents.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

    return (
        "Agent stopped because it reached the maximum "
        f"of {max_steps} steps. Please try a simpler query."
    )


if __name__ == "__main__":
    while True:
        query = input("\nYou: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        try:
            answer = run_agent(query)
            print("\nAgent:", answer)
        except Exception:
            logger.exception("Agent request failed")
            print("Agent: Something went wrong. Check the logs.")
