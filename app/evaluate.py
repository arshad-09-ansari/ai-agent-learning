evaluation_data = [
    {
        "question": "How many paid leaves do employees get?",
        "relevant_chunk": "Employees receive 20 paid leaves per year."
    },
    {
        "question": "Can employees work from home?",
        "relevant_chunk": "Employees can work from home two days per week."
    }
]
retrieved_chunks = [
    "Employees receive 20 paid leaves per year.",
    "Employees can work from home two days per week.",
    "Employees receive medical insurance."
]
def precision_at_k(retrieved, relevant, k):

    top_k = retrieved[:k]

    relevant_count = sum(
        1 for chunk in top_k
        if chunk == relevant
    )

    return relevant_count / k

retrieved = [
    "salary policy",
    "leave policy",
    "insurance policy"
]

relevant = "leave policy"

score = precision_at_k(
    retrieved,
    relevant,
    3
)

print(score)