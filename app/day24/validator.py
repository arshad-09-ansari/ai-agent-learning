# LLM kabhi-kabhi missing arguments, extra arguments ya wrong data types de sakta hai.


from numbers import Real


TOOL_SCHEMAS = {
    "add": {
        "required": {"a": Real, "b": Real},
        "optional": {},
    },
    "multiply": {
        "required": {"a": Real, "b": Real},
        "optional": {},
    },
    "subtract": {
    "required": {"a": Real, "b": Real},
    "optional": {},
    },
    "knowledge_search": {
        "required": {"query": str},
        "optional": {},
    },
}


def validate_arguments(
    tool_name: str,
    arguments: dict,
) -> None:
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary.")

    schema = TOOL_SCHEMAS.get(tool_name)

    if schema is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    required = schema["required"]
    optional = schema["optional"]

    allowed_names = set(required) | set(optional)
    supplied_names = set(arguments)

    missing = set(required) - supplied_names
    extra = supplied_names - allowed_names

    if missing:
        raise ValueError(
            f"Missing arguments: {sorted(missing)}"
        )

    if extra:
        raise ValueError(
            f"Unexpected arguments: {sorted(extra)}"
        )

    for name, expected_type in required.items():
        value = arguments[name]

        # bool is a subclass of int in Python.
        # Explicitly reject it for numeric arguments.
        if expected_type is Real and isinstance(value, bool):
            raise ValueError(
                f"{name} must be a number, not a boolean."
            )

        if not isinstance(value, expected_type):
            raise ValueError(
                f"{name} must have type "
                f"{expected_type.__name__}."
            )

    for name, expected_type in optional.items():
        if name in arguments:
            if not isinstance(arguments[name], expected_type):
                raise ValueError(
                    f"{name} must have type "
                    f"{expected_type.__name__}."
                )

    
    for name, expected_type in required.items():
        value = arguments[name]

        if expected_type is Real:
            if isinstance(value, bool):
                raise ValueError(
                    f"{name} must be a number, not a boolean."
                )

            if not isinstance(value, Real):
                raise ValueError(
                    f"{name} must be a number."
                )

            if not math.isfinite(value):
                raise ValueError(
                    f"{name} must be finite."
                )

        elif not isinstance(value, expected_type):
            raise ValueError(
                f"{name} must have type "
                f"{expected_type.__name__}."
            )



# multiply
# Valid

# {"a": 10, "b": 5}


# multiply
# Missing b

# {"a": 10}


# multiply
# Invalid type

# {"a": 10, "b": "five"}


# delete_database
# Unknown tool

# {}


# add
# Unexpected argument

# {"a": 2, "b": 3, "admin": true}