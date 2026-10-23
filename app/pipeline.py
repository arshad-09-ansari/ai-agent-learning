def rag_pipeline(query):

    # 1. Convert query into embedding
    query_embedding = create_embedding(query)

    # 2. Retrieve candidates
    candidates = retrieve(query_embedding, top_k=20)

    # 3. Rerank candidates
    ranked = rerank(query, candidates)

    # 4. Select best chunks
    context = ranked[:5]

    # 5. Send context to LLM
    answer = generate_answer(query, context)

    return answer