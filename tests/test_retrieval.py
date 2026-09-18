from rag.retrieval import search_documents


def test_finance_user_retrieves_q4_forecast():
    results = search_documents(
        "U102",
        "Q4 revenue forecast"
    )

    document_ids = [doc["document_id"] for doc in results]

    assert "DOC-101" in document_ids


def test_marketing_user_cannot_retrieve_restricted_revenue():
    results = search_documents(
        "U205",
        "Q4 revenue forecast"
    )

    document_ids = [doc["document_id"] for doc in results]

    assert "DOC-201" not in document_ids


def test_retrieval_never_returns_unauthorized_content():
    results = search_documents(
        "U205",
        "Q4 revenue forecast"
    )

    for document in results:
        assert document["document_id"] != "DOC-201"
        assert "145 crore" not in document["content"]


def test_finance_user_retrieves_both_forecast_versions():
    results = search_documents(
        "U301",
        "Q4 forecast"
    )

    document_ids = [doc["document_id"] for doc in results]

    assert "DOC-301" in document_ids
    assert "DOC-302" in document_ids