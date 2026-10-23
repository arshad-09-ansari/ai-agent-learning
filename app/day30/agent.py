
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.day30.tools import execute_tool

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)


# Tell Gemini which tools it can request.
tool_definitions = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculator",
            description="Calculate two numbers.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "operation": types.Schema(
                        type="STRING",
                        enum=[
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ]
                    ),
                    "a": types.Schema(type="NUMBER"),
                    "b": types.Schema(type="NUMBER"),
                },
                required=["operation", "a", "b"],
            ),
        ),
        types.FunctionDeclaration(
            name="knowledge_search",
            description=(
                "Search the knowledge base for information "
                "about Redis, RabbitMQ, Spring Boot or RAG."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(type="STRING"),
                },
                required=["query"],
            ),
        ),
    ]
)


def ask_agent(user_query, history):
    # Add the current user message to conversation history.
    history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)],
        )
    )

    # Limit tool rounds to prevent an endless agent loop.
    for step in range(5):

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=history,
            config=types.GenerateContentConfig(
                tools=[tool_definitions],
                system_instruction=(
                    "You are a helpful AI assistant. "
                    "Use calculator for mathematical calculations. "
                    "Use knowledge_search when relevant knowledge "
                    "is required. Never invent tool results. "
                    "After receiving tool results, answer clearly."
                ),
            ),
        )

        if not response.candidates:
            return "The model returned no usable response."

        model_content = response.candidates[0].content

        # Preserve the model response, including any function calls.
        history.append(model_content)

        function_calls = response.function_calls

        # No tool request means the model has finished answering.
        if not function_calls:
            return response.text or "No text response was returned."

        # Execute every requested tool call.
        for function_call in function_calls:
            try:
                arguments = function_call.args or {}

                print(
                    f"\nTool requested: {function_call.name}"
                )
                print(f"Arguments: {arguments}")

                result = execute_tool(
                    function_call.name,
                    arguments,
                )

            except Exception:
                result = {
                    "ok": False,
                    "error": "Tool execution failed"
                }

            print("Tool result:", result)

            # Send the result back to Gemini.
            history.append(
                types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call.name,
                            response=result,
                        )
                    ],
                )
            )

    return (
        "Maximum tool rounds reached. "
        "Please try a simpler query."
    )


def main():
    history = []

    print("Day 30 AI Agent")
    print("Type 'exit' to stop.\n")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in {"exit", "quit"}:
            break

        if not user_query:
            continue

        try:
            answer = ask_agent(user_query, history)
            print("\nAgent:", answer, "\n")

        except Exception as exc:
            print("\nAgent error:", str(exc), "\n")


if __name__ == "__main__":
    main()
