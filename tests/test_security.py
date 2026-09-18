from agent.research_agent import research


def test_authorized_user_gets_answer():
    result = research(
        "U102",
        "Q4 revenue forecast"
    )

    assert result["status"] == "success"
    assert "120 crore" in result["answer"]
    assert result["sources"][0]["document_id"] == "DOC-101"


def test_unauthorized_user_does_not_get_restricted_answer():
    result = research(
        "U205",
        "Q4 revenue forecast"
    )

    assert result["status"] == "no_accessible_evidence"
    assert "145 crore" not in result["answer"]


def test_latest_authorized_version_is_used():
    result = research(
        "U301",
        "Q4 forecast"
    )

    assert result["status"] == "success"
    assert "125 crore" in result["answer"]
    assert result["sources"][0]["document_id"] == "DOC-302"


def test_unknown_user_gets_no_answer():
    result = research(
        "U999",
        "Q4 revenue forecast"
    )

    assert result["status"] == "no_accessible_evidence"