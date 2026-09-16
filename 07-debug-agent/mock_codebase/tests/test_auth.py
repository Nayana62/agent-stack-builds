import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import authenticate, is_admin


def test_authenticate_valid_user():
    result = authenticate("alice@example.com", "secret123")
    assert result["email"] == "alice@example.com"
    assert result["name"] == "Alice"
    assert result["role"] == "admin"


def test_authenticate_invalid_password():
    try:
        authenticate("alice@example.com", "wrong")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Invalid password"


def test_is_admin():
    profile = authenticate("alice@example.com", "secret123")
    assert is_admin(profile) is True


def test_non_admin():
    profile = authenticate("bob@example.com", "pass456")
    assert is_admin(profile) is False


if __name__ == "__main__":
    tests = [
        test_authenticate_valid_user,
        test_authenticate_invalid_password,
        test_is_admin,
        test_non_admin,
    ]
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")
