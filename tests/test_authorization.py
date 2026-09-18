def test_clearance_must_match_document_classification():
    user = {
        "user_id": "U102",
        "role": "Finance",
        "department": "Finance",
        "clearance": "Internal"
    }

    restricted_document = {
        "document_id": "DOC-999",
        "title": "Restricted Finance Document",
        "classification": "Restricted",
        "allowed_departments": ["Finance"],
        "allowed_roles": ["Finance"],
        "version": "1.0",
        "effective_date": "2026-09-01",
        "content": "Restricted information."
    }

    from auth.authorization import can_access

    assert can_access(user, restricted_document) is False