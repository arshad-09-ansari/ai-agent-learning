chunks = [
    """
    Users can request a refund within 7 days of purchase.
    Refunds are processed within 5 business days.
    """,

    """
    Our company was founded in 2012.
    We currently have offices in Delhi and Mumbai.
    """,

    """
    Users can cancel an order before it is shipped.
    """,

    """
    Refund requests must include the original order ID.
    """
]

query = "How many days do I have to request a refund?"

def compress_context(chunks, query):
    keywords = query.lower().split()

    relevant = []

    for chunk in chunks:
        text = chunk.lower()

        score = sum(
            1 for keyword in keywords
            if keyword in text
        )

        if score > 0:
            relevant.append(chunk)

    return relevant

compressed = compress_context(chunks, query)

for chunk in compressed:
    print(chunk)