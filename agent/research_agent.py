from rag.retrieval import search_documents
from services.versioning import get_latest_version


def research(user_id, query):
    results = search_documents(user_id, query)

    if not results:
        return {
            "status": "no_accessible_evidence",
            "answer": "No accessible information was found for this question.",
            "sources": []
        }

    latest_document = get_latest_version(results)

    return {
        "status": "success",
        "answer": latest_document["content"],
        "sources": [
            {
                "document_id": latest_document["document_id"],
                "title": latest_document["title"],
                "version": latest_document["version"],
                "effective_date": latest_document["effective_date"]
            }
        ]
    }