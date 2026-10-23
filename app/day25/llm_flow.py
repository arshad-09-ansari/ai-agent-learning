from app.day25.agent import build_agent


def mock_llm(user_query: str) -> dict:
    """
    Simulates an LLM tool-call response.
    This is NOT a real LLM.
    """

    if "125" in user_query and "8" in user_query:
        return {
            "type": "tool_call",
            "name": "multiply",
            "arguments": {
                "a": 125,
                "b": 8
            }
        }

    return {
        "type": "final",
        "answer": "I could not determine the required action."
    }


def run_agent(user_query: str):
    dispatcher = build_agent()

    response = mock_llm(user_query)

    if response["type"] == "tool_call":
        tool_result = dispatcher.execute(
            response["name"],
            response["arguments"]
        )

        if not tool_result["ok"]:
            return {
                "answer": "The requested tool could not be executed.",
                "tool_result": tool_result
            }

        # A real implementation would send the tool result
        # back to the LLM using the provider's tool-response format.
        return {
            "answer": f"The result is {tool_result['result']}.",
            "tool_result": tool_result
        }

    return {"answer": response["answer"]}


if __name__ == "__main__":
    print(run_agent("Calculate 125 multiplied by 8"))