import logging

from app.day25.agent import build_agent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def main():
    dispatcher = build_agent()

    test_cases = [
        ("multiply", {"a": 125, "b": 8}),
        ("divide", {"a": 10, "b": 2}),
        ("divide", {"a": 10, "b": 0}),
        ("multiply", {"a": 10}),
        ("multiply", {"a": 10, "b": 5, "c": 2}),
        ("multiply", {"a": "ten", "b": 5}),
        ("unknown_tool", {}),
        ("search_knowledge", {"query": "What is Redis?"})
    ]

    for tool_name, arguments in test_cases:
        print("\n" + "=" * 50)
        print("TOOL:", tool_name)
        print("ARGUMENTS:", arguments)

        result = dispatcher.execute(
            tool_name,
            arguments
        )

        print("RESULT:", result)


if __name__ == "__main__":
    main()