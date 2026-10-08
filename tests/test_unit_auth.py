import pytest
from app.models.user import User
from app.core.security import validate_username, validate_email, validate_password_strength

def test_password_hashing_and_verification(app):
    """TEST-01: Verify bcrypt password hashing produces unique salted hashes and verifies accurately."""
    with app.app_context():
        user = User(username="charlie", email="charlie@test.local")
        user.set_password("SecurePassword2026!")

        assert user.password_hash is not None
        assert user.password_hash.startswith("$2b$")
        assert user.check_password("SecurePassword2026!") is True
        assert user.check_password("WrongPassword!") is False
        assert user.check_password("") is False

def test_password_minimum_length_enforcement(app):
    """TEST-01: Verify password shorter than 8 characters is rejected."""
    with app.app_context():
        user = User(username="charlie", email="charlie@test.local")
        with pytest.raises(ValueError, match="at least 8 characters"):
            user.set_password("short")

def test_username_validation():
    """Verify username whitelist constraints."""
    valid, _ = validate_username("alice_99")
    assert valid is True

    valid, _ = validate_username("ab")  # Too short
    assert valid is False

    valid, _ = validate_username("user<script>")  # Malicious chars
    assert valid is False

def test_email_validation():
    """Verify email format validation."""
    valid, _ = validate_email("alice@platform.local")
    assert valid is True

    valid, _ = validate_email("invalid-email-address")
    assert valid is False
