from retrievers import (
    vector_search,
    sql_search,
    api_search
)


def retrieve_from_routes(query, routes):

    context = []

    for route in routes:

        if route == "vector":
            result = vector_search(query)

        elif route == "sql":
            result = sql_search(query)

        elif route == "api":
            result = api_search(query)

        else:
            continue

        context.extend(result)

    return context 