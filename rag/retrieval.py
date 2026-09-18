from auth.authorization import get_authorized_documents


def search_documents(user_id, query):
    authorized_documents = get_authorized_documents(user_id)

    query_lower = query.lower().strip()
    query_words = set(query_lower.split())
    results = []

    for document in authorized_documents:
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
                "content": document["content"],
                "score": score
            })

    results.sort(
        key=lambda document: document["score"],
        reverse=True
    )

    return results