from datetime import datetime


def get_latest_version(documents):
    if not documents:
        return None

    return max(
        documents,
        key=lambda document: (
            datetime.strptime(
                document["effective_date"],
                "%Y-%m-%d"
            ),
            float(document["version"])
        )
    )