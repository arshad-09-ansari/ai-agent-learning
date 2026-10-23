
from app.day24.dispatcher import dispatch
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

def main():
    result1 = dispatch(
        "multiply",
        {"a": 250, "b": 4},
    )
    print("Calculation:", result1)

    result2 = dispatch(
        "knowledge_search",
        {"query": "What is Redis?"},
    )
    print("Knowledge:", result2)

    result3 = dispatch(
        "delete_database",
        {},
    )
    print("Unauthorized tool:", result3)

    result4 = dispatch(
        "multiply",
        {"a": 250},
    )
    print("Invalid arguments:", result4)


if __name__ == "__main__":
    main()
