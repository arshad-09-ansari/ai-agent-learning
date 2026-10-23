# def generate_queries(query):

#     return [
#         query,
#         query + " best practices",
#         query + " common problems",
#         query + " performance optimization"
#     ]

def generate_queries(user_query):

    prompt = f"""
    Generate 3 different search queries
    that can retrieve relevant information
    for this question.

    Question:
    {user_query}
    """

    # LLM call here

    return queries
if __name__ == "__main__":

    query = "Why is my Spring Boot application slow?"

    queries = generate_queries(query)

    for i, q in enumerate(queries, 1):
        print(f"{i}. {q}")