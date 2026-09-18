from rag.retrieval import search_documents
from services.versioning import get_latest_version
from services.llm import prepare_llm_request, generate_answer
from services.audit import log_request

def research(user_id, query):
    results = search_documents(user_id, query)

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