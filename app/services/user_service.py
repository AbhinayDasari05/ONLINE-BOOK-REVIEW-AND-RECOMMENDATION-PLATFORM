from app.extensions import db
from app.models.user import User
from app.core.security import validate_username, validate_email, validate_password_strength
from app.core.audit import log_audit_event

class UserService:
    """User account and authentication service (COMP-01, COMP-02)."""

    @staticmethod
    def register_user(username: str, email: str, password: str, is_admin: bool = False) -> tuple[bool, str, User or None]:
        """Register a new user with input validation and duplicate checking (REQ-01)."""
        valid_u, u_err = validate_username(username)
        if not valid_u:
            return False, u_err, None

        valid_e, e_err = validate_email(email)
        if not valid_e:
            return False, e_err, None

        valid_p, p_err = validate_password_strength(password)
        if not valid_p:
            return False, p_err, None

        if User.query.filter_by(username=username).first():
            return False, "Username is already registered.", None

        if User.query.filter_by(email=email).first():
            return False, "Email address is already in use.", None

        try:
            user = User(
                username=username,
                email=email,
                is_admin=is_admin
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            log_audit_event("USER_REGISTRATION", "User", user.id, "SUCCESS", f"User registered: {username}", user=user)
            return True, "Registration successful.", user
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed due to a server error.", None

    @staticmethod
    def authenticate_user(username_or_email: str, password: str) -> tuple[bool, str, User or None]:
        """Authenticate user by username or email with secure bcrypt comparison (REQ-02)."""
        if not username_or_email or not password:
            return False, "Username and password are required.", None

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if not user or not user.check_password(password):
            log_audit_event("AUTH_FAILURE", "User", None, "FAILURE", f"Failed login attempt for: {username_or_email}")
            return False, "Invalid username or password.", None

        log_audit_event("AUTH_SUCCESS", "User", user.id, "SUCCESS", f"User authenticated: {user.username}", user=user)
        return True, "Login successful.", user
