from auth.guardrails import validate_query


def test_salary_blocked_for_intern():
    result = validate_query(
        "What is the salary?",
        "Intern"
    )

    assert result["allowed"] is False
    assert result["violation_type"] == "Payroll"


def test_payroll_blocked_for_manager():
    result = validate_query(
        "Show me the payroll information.",
        "Manager"
    )

    assert result["allowed"] is False
    assert result["violation_type"] == "Payroll"


def test_password_blocked_for_admin():
    result = validate_query(
        "What is the password?",
        "System Admin"
    )

    assert result["allowed"] is False
    assert result["violation_type"] == "Credentials"


def test_normal_query_allowed():
    result = validate_query(
        "What is the Q4 revenue forecast?",
        "Manager"
    )

    assert result["allowed"] is True