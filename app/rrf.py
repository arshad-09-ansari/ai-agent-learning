def reciprocal_rank_fusion(result_lists, k=60):

    scores = {}

    for results in result_lists:

        for rank, document_id in enumerate(results, start=1):

            score = 1 / (k + rank)

            scores[document_id] = scores.get(document_id, 0) + score

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


vector_results = [
    "doc_3",
    "doc_8",
    "doc_1",
    "doc_4",
    "doc_6"
]

bm25_results = [
    "doc_3",
    "doc_1",
    "doc_8",
    "doc_7",
    "doc_10"
]


final_results = reciprocal_rank_fusion(
    [
        vector_results,
        bm25_results
    ]
)


print("Hybrid Results:\n")

for document_id, score in final_results:
    print(document_id, round(score, 5))