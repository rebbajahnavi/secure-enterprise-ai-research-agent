from rag.retrieval import search_documents


def test_intern_cannot_retrieve_internal_document():
    results = search_documents(
        "U102",
        "Q4 revenue forecast",
        "Intern"
    )

    document_ids = [
        document["document_id"]
        for document in results
    ]

    assert "DOC-101" not in document_ids


def test_manager_can_retrieve_internal_document():
    results = search_documents(
        "U102",
        "Q4 revenue forecast",
        "Manager"
    )

    document_ids = [
        document["document_id"]
        for document in results
    ]

    assert "DOC-101" in document_ids


def test_security_level_is_not_above_role():
    results = search_documents(
        "U102",
        "Q4 revenue forecast",
        "Manager"
    )

    for document in results:
        assert document["security_level"] <= 2