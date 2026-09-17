from database import get_user_by_email


def authenticate(email: str, password: str) -> dict:
    """Authenticate a user and return their profile with role."""
    user = get_user_by_email(email)

    if user is None:
        raise ValueError("User not found")

    if user["password"] != password:
        raise ValueError("Invalid password")

    return {
        "email": user["email"],
        "name": user.get("name"),
        "role": user.get("role"),
    }


def is_admin(user_profile: dict) -> bool:
    """Check if authenticated user is an admin."""
    return user_profile.get("role") == "admin"
