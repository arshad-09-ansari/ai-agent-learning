
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.day26.tools import execute_tool


# 1. Load configuration
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


# 2. Describe tools available to Gemini
tool_definitions = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="multiply",
                description="Multiply two numbers.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "a": types.Schema(type=types.Type.NUMBER),
                        "b": types.Schema(type=types.Type.NUMBER),
                    },
                    required=["a", "b"],
                ),
            ),
            types.FunctionDeclaration(
                name="add",
                description="Add two numbers.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "a": types.Schema(type=types.Type.NUMBER),
                        "b": types.Schema(type=types.Type.NUMBER),
                    },
                    required=["a", "b"],
                ),
            ),
        ]
    )
]


def run_agent(user_query: str) -> str:
    # 3. Start conversation
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)],
        )
    ]

    config = types.GenerateContentConfig(
        tools=tool_definitions,
        system_instruction=(
            "You are a helpful assistant. "
            "Use available tools when calculations are required. "
            "Never claim a tool succeeded unless its result confirms success."
        ),
        temperature=0,
    )

    # 4. First request to Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )

    max_steps = 5

    # 5. Agent loop
    for step in range(max_steps):
        if not response.candidates:
            return "The model returned no usable response."

        model_content = response.candidates[0].content

        if model_content is None:
            return "The model returned no response content."

        function_calls = [
            part.function_call
            for part in (model_content.parts or [])
            if part.function_call is not None
        ]

        # No tool call: return final answer
        if not function_calls:
            return response.text or "No text answer was returned."

        # Preserve Gemini's tool-call message
        contents.append(model_content)

        function_response_parts = []

        # 6. Execute all requested tools
        for function_call in function_calls:
            name = function_call.name
            arguments = dict(function_call.args or {})

            print(f"Tool requested: {name}")
            print(f"Arguments: {arguments}")

            result = execute_tool(name, arguments)

            print(f"Tool result: {result}")

            function_response_parts.append(
                types.Part.from_function_response(
                    name=name,
                    response=result,
                )
            )

        # 7. Send tool results back to Gemini
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts,
            )
        )

        # 8. Ask Gemini to continue
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )

    return "Agent stopped: maximum tool rounds reached."


# 9. Program entry point
if __name__ == "__main__":
    query = input("Ask your agent: ").strip()

    if not query:
        print("Please enter a question.")
    else:
        try:
            answer = run_agent(query)
            print("\nFinal answer:")
            print(answer)
        except Exception as exc:
            print(f"Agent request failed: {type(exc).__name__}")
            # In production, log the exception securely.
