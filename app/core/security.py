import re
import html
from functools import wraps
from flask import abort, request, redirect, url_for, flash
from flask_login import current_user

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_.-]{3,30}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def admin_required(f):
    """RBAC decorator enforcing administrator privileges (CTRL-06, REQ-10, REQ-11)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Authentication required to access administrator features.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin:
            # Deny non-admin users with 403 Forbidden
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def validate_username(username: str) -> tuple[bool, str]:
    """Validate username against strict alphanumeric whitelist."""
    if not username or not isinstance(username, str):
        return False, "Username is required."
    username = username.strip()
    if len(username) < 3 or len(username) > 30:
        return False, "Username must be between 3 and 30 characters."
    if not USERNAME_REGEX.match(username):
        return False, "Username may only contain letters, numbers, hyphens, and underscores."
    return True, username

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email address format and bounds."""
    if not email or not isinstance(email, str):
        return False, "Email address is required."
    email = email.strip().lower()
    if len(email) > 120:
        return False, "Email address is too long."
    if not EMAIL_REGEX.match(email):
        return False, "Invalid email address format."
    return True, email

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Enforce minimum password security policy."""
    if not password or not isinstance(password, str):
        return False, "Password is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if len(password) > 128:
        return False, "Password must not exceed 128 characters."
    return True, password

def validate_rating(rating_val) -> tuple[bool, int]:
    """Enforce integer rating between 1 and 5 (REQ-05)."""
    try:
        val = int(rating_val)
        if 1 <= val <= 5:
            return True, val
        return False, 0
    except (ValueError, TypeError):
        return False, 0

def sanitize_text(text: str, max_length: int = 2000) -> str:
    """Trim, enforce length bound, and strip null bytes."""
    if not text:
        return ""
    text = str(text).replace('\x00', '').strip()
    if len(text) > max_length:
        text = text[:max_length]
    return text
