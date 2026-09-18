import json
from datetime import datetime

AUDIT_FILE = "data/audit_log.json"

def log_request(
    user_id,
    query,
    status,
    sources,
    authorization_decision,
    llm_evidence_ids
):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "query": query,
        "status": status,
        "authorization_decision": authorization_decision,
        "llm_evidence_ids": llm_evidence_ids,
        "sources": sources
    }

    try:
        with open(AUDIT_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(entry)

    with open(AUDIT_FILE, "w") as file:
        json.dump(logs, file, indent=2)