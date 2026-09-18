from auth.authorization import get_authorized_documents
from auth.rbac import get_role_level


def search_documents(user_id, query, role=None):
    authorized_documents = get_authorized_documents(user_id)

    if role is None:
        user_security_level = 4
    else:
        user_security_level = get_role_level(role)

    query_lower = query.lower().strip()
    query_words = set(query_lower.split())

    results = []

    for document in authorized_documents:
        document_security_level = document.get(
            "security_level",
            1
        )

        if document_security_level > user_security_level:
            continue

        title = document["title"].lower()
        content = document["content"].lower()

        score = 0

        for word in query_words:
            if word in title:
                score += 2
            elif word in content:
                score += 1

        if query_lower in title:
            score += 5

        if score > 0:
            results.append({
                "document_id": document["document_id"],
                "title": document["title"],
                "version": document["version"],
                "effective_date": document["effective_date"],
                "security_level": document_security_level,
                "content": document["content"],
                "score": score
            })

    results.sort(
        key=lambda document: document["score"],
        reverse=True
    )

    return results