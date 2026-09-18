from auth.authorization import get_user, can_access, get_authorized_documents


def test_finance_user_can_access_finance_document():
    user = get_user("U102")
    documents = get_authorized_documents("U102")

    assert user is not None
    assert any(doc["document_id"] == "DOC-101" for doc in documents)


def test_marketing_user_cannot_access_restricted_document():
    documents = get_authorized_documents("U205")

    assert not any(doc["document_id"] == "DOC-201" for doc in documents)


def test_finance_user_can_access_finance_documents():
    documents = get_authorized_documents("U301")

    document_ids = [doc["document_id"] for doc in documents]

    assert "DOC-301" in document_ids
    assert "DOC-302" in document_ids


def test_unknown_user_has_no_access():
    documents = get_authorized_documents("U999")

    assert documents == []