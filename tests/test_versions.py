from services.versioning import get_latest_version


def test_latest_authorized_version():
    documents = [
        {
            "document_id": "DOC-301",
            "version": "1.0",
            "effective_date": "2026-06-01",
            "content": "Q4 projected revenue is 110 crore."
        },
        {
            "document_id": "DOC-302",
            "version": "2.0",
            "effective_date": "2026-09-01",
            "content": "Q4 projected revenue is 125 crore."
        }
    ]

    latest = get_latest_version(documents)

    assert latest["document_id"] == "DOC-302"
    assert latest["version"] == "2.0"
    assert latest["content"] == "Q4 projected revenue is 125 crore."


def test_empty_documents_returns_none():
    latest = get_latest_version([])

    assert latest is None