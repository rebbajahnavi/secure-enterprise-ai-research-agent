import json

def load_users():
    with open("data/users.json", "r") as file:
        return json.load(file)

def load_documents():
    with open("data/documents.json", "r") as file:
        return json.load(file)

def get_user(user_id):
    users = load_users()

    for user in users:
        if user["user_id"] == user_id:
            return user

    return None

def can_access(user, document):
    if user is None:
        return False

    department_allowed = (
        user["department"] in document["allowed_departments"]
    )

    role_allowed = (
        user["role"] in document["allowed_roles"]
    )

    return department_allowed and role_allowed

def get_authorized_documents(user_id):
    user = get_user(user_id)

    if user is None:
        return []

    documents = load_documents()

    return [
        document
        for document in documents
        if can_access(user, document)
    ]