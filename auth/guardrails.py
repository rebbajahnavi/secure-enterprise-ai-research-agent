FORBIDDEN_KEYWORDS = {
    "salary": "Payroll",
    "payroll": "Payroll",
    "password": "Credentials",
    "passwords": "Credentials",
    "pii": "PII",
    "personal information": "PII",
    "ceo home address": "Executive Private",
    "executive private": "Executive Private"
}

def validate_query(query, role):
    query_lower = query.lower()

    for keyword, violation_type in FORBIDDEN_KEYWORDS.items():
        if keyword in query_lower:

            if violation_type == "Credentials":
                return {
                    "allowed": False,
                    "violation_type": violation_type,
                    "message": "Security Violation: Access to credentials is blocked."
                }

            if violation_type not in {
                "Payroll",
                "PII",
                "Executive Private"
            }:
                continue

            allowed = (
                role in ["HR Admin", "System Admin"]
            )

            if not allowed:
                return {
                    "allowed": False,
                    "violation_type": violation_type,
                    "message": "Security Violation: You do not have permission to access this information."
                }

    return {
        "allowed": True,
        "violation_type": None,
        "message": None
    }