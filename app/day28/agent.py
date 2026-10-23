
import os
import json
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.day28.tools import execute_tool

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)

tool_declarations = [
    types.FunctionDeclaration(
        name="add",
        description="Add two numbers.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {"type": "NUMBER"},
                "b": {"type": "NUMBER"},
            },
            "required": ["a", "b"],
        },
    ),
    types.FunctionDeclaration(
        name="multiply",
        description="Multiply two numbers.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {"type": "NUMBER"},
                "b": {"type": "NUMBER"},
            },
            "required": ["a", "b"],
        },
    ),
    types.FunctionDeclaration(
        name="subtract",
        description="Subtract b from a.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "a": {"type": "NUMBER"},
                "b": {"type": "NUMBER"},
            },
            "required": ["a", "b"],
        },
    ),
]

tools = [
    types.Tool(function_declarations=tool_declarations)
]

config = types.GenerateContentConfig(
    tools=tools,
    temperature=0,
    system_instruction=(
        "You are a calculation agent. "
        "Use the provided tools for calculations. "
        "For multi-step calculations, use the result "
        "of one tool as input to the next tool. "
        "Never invent tool results. "
        "If a tool fails, explain the failure."
    ),
)


def run_agent(user_query: str, max_steps: int = 6) -> str:
    chat = client.chats.create(
        model=MODEL_NAME,
        config=config,
    )

    response = chat.send_message(user_query)

    for step in range(1, max_steps + 1):
        function_calls = response.function_calls or []

        # No more tool calls: return the final answer.
        if not function_calls:
            return response.text or "No final text returned."

        logging.info(
            "Agent step %s: %s tool call(s)",
            step,
            len(function_calls),
        )

        function_responses = []

        for call in function_calls:
            tool_name = call.name
            arguments = dict(call.args or {})

            print(
                f"\nExecuting: {tool_name}"
                f"\nArguments: {arguments}"
            )

            result = execute_tool(tool_name, arguments)

            print("Tool result:", result)

            function_responses.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response=result,
                )
            )

        # Send tool results back to Gemini.
        response = chat.send_message(
            function_responses
        )

    return (
        "Maximum agent steps reached. "
        "The task could not be completed within the limit."
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
            logging.exception("Agent execution failed")
            print("Agent failed. Check the logs.")
