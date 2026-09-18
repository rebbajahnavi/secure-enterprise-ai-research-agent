def test_unauthorized_content_never_reaches_llm():
    from services.llm import prepare_llm_request
    from rag.retrieval import search_documents

    results = search_documents(
        "U205",
        "What is the Q4 revenue forecast?"
    )

    request = prepare_llm_request(
        "What is the Q4 revenue forecast?",
        results
    )

    assert request is None