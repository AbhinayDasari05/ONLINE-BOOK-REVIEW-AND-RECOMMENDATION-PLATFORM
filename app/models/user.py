import bcrypt
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    """User entity for authentication and role-based access control (COMP-01, COMP-02)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships with explicit foreign_keys disambiguation
    reviews = db.relationship('Review', foreign_keys='Review.user_id', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    reading_list_items = db.relationship('ReadingListItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='actor', lazy='dynamic')

    def set_password(self, password: str):
        """Hash password securely using Bcrypt (CTRL-01, REQ-02)."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password against Bcrypt hash (CTRL-01)."""
        if not self.password_hash or not password:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception:
            return False

    def __repr__(self):
        return f"<User {self.username} (Admin: {self.is_admin})>"
