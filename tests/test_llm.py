from services.llm import prepare_llm_request


def test_authorized_content_is_sent_to_llm():
    evidence = [
        {
            "document_id": "DOC-101",
            "title": "Q4 Revenue Forecast",
            "version": "2.0",
            "content": "Q4 projected revenue is 120 crore."
        }
    ]

    request = prepare_llm_request(
        "What is the Q4 revenue forecast?",
        evidence
    )

    assert request is not None
    assert "120 crore" in request["prompt"]
    assert "DOC-101" in request["prompt"]


def test_unauthorized_content_is_not_sent_to_llm():
    evidence = [
        {
            "document_id": "DOC-101",
            "title": "Q4 Revenue Forecast",
            "version": "2.0",
            "content": "Q4 projected revenue is 120 crore."
        }
    ]

    request = prepare_llm_request(
        "What is the Q4 revenue forecast?",
        evidence
    )

    assert "145 crore" not in request["prompt"]


def test_empty_evidence_is_not_sent_to_llm():
    request = prepare_llm_request(
        "What is the Q4 revenue forecast?",
        []
    )

    assert request is None