
from services.security_audit import log_security_violation
from auth.guardrails import validate_query
from rag.retrieval import search_documents
from services.versioning import get_latest_version
from services.llm import prepare_llm_request, generate_answer
from services.audit import log_request

def research(user_id, query, role="Intern"):
    validation = validate_query(query, role)

    if not validation["allowed"]:
        result = {
            "status": "security_violation",
            "answer": validation["message"],
            "sources": [],
            "llm_request": None,
            "violation_type": validation["violation_type"]
        }

        log_security_violation(
        role,
        query,
        validation["violation_type"]
        )

        log_request(
            user_id,
            query,
            result["status"],
            [],
            "blocked",
            []
        )

        return result

    results = search_documents(user_id, query, role)

    if not results:
        result = {
            "status": "no_accessible_evidence",
            "answer": "No accessible information was found for this question.",
            "sources": [],
            "llm_request": None
        }

        log_request(
            user_id,
            query,
            result["status"],
            result["sources"],
            "denied",
            []
        )

        return result

    latest_document = get_latest_version(results)
    evidence = [latest_document]

    llm_request = prepare_llm_request(query, evidence)
    answer = generate_answer(query, evidence)

    result = {
        "status": "success",
        "answer": answer,
        "sources": [
            {
                "document_id": latest_document["document_id"],
                "title": latest_document["title"],
                "version": latest_document["version"],
                "effective_date": latest_document["effective_date"]
            }
        ],
        "llm_request": llm_request
    }

    log_request(
        user_id,
        query,
        result["status"],
        result["sources"],
        "authorized",
        [latest_document["document_id"]]
    )

    return result