ROLE_LEVELS = {
    "Intern": 1,
    "Manager": 2,
    "HR Admin": 3,
    "System Admin": 4
}

ROLE_PERMISSIONS = {
    "Intern": ["Public", "Internal"],
    "Manager": ["Public", "Internal", "Confidential"],
    "HR Admin": ["Public", "Internal", "Confidential", "Payroll"],
    "System Admin": ["Public", "Internal", "Confidential", "Payroll", "System"]
}

def get_role_level(role):
    return ROLE_LEVELS.get(role, 0)

def has_permission(role, category):
    return category in ROLE_PERMISSIONS.get(role, [])