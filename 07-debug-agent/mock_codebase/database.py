USERS_DB = [
    {
        "email": "alice@example.com",
        "name": "Alice",
        "password": "secret123",
        "user_role": "admin",
    },
    {
        "email": "bob@example.com",
        "name": "Bob",
        "password": "pass456",
        "user_role": "viewer",
    },
]


def get_user_by_email(email: str) -> dict | None:
    """Look up a user by email address."""
    for user in USERS_DB:
        if user["email"] == email:
            return user
    return None


def get_all_users() -> list[dict]:
    """Return all users in the database."""
    return USERS_DB
