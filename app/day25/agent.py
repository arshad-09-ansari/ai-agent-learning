from app.day25.registry import (
    ToolDefinition,
    ToolRegistry
)
from app.day25.dispatcher import ToolDispatcher
from app.day25.tools import (
    add,
    multiply,
    divide,
    search_knowledge
)


def build_agent() -> ToolDispatcher:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="add",
            description="Add two numbers",
            function=add,
            argument_types={
                "a": float,
                "b": float
            },
            required_args=("a", "b")
        )
    )

    registry.register(
        ToolDefinition(
            name="multiply",
            description="Multiply two numbers",
            function=multiply,
            argument_types={
                "a": float,
                "b": float
            },
            required_args=("a", "b")
        )
    )

    registry.register(
        ToolDefinition(
            name="divide",
            description="Divide the first number by the second",
            function=divide,
            argument_types={
                "a": float,
                "b": float
            },
            required_args=("a", "b")
        )
    )

    registry.register(
        ToolDefinition(
            name="search_knowledge",
            description="Search the local knowledge base",
            function=search_knowledge,
            argument_types={
                "query": str
            },
            required_args=("query",)
        )
    )

    print("Registered tools:", registry.list_tools())

    return ToolDispatcher(registry)