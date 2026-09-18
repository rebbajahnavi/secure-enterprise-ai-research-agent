import os
import pandas as pd
from datetime import datetime

AUDIT_FILE = "data/security_audit.csv"

COLUMNS = [
    "Timestamp",
    "User Role",
    "Query",
    "Violation Type"
]

def log_security_violation(role, query, violation_type):
    os.makedirs("data", exist_ok=True)

    new_entry = pd.DataFrame([{
        "Timestamp": datetime.now().isoformat(),
        "User Role": role,
        "Query": query,
        "Violation Type": violation_type
    }])

    if os.path.exists(AUDIT_FILE):
        existing_logs = pd.read_csv(AUDIT_FILE)
        logs = pd.concat(
            [existing_logs, new_entry],
            ignore_index=True
        )
    else:
        logs = new_entry

    logs.to_csv(AUDIT_FILE, index=False)

def load_security_audit():
    if not os.path.exists(AUDIT_FILE):
        return pd.DataFrame(columns=COLUMNS)

    return pd.read_csv(AUDIT_FILE)