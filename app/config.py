import os
import secrets

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)

class Config:
    """Base configuration with security-first defaults."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    default_db_path = os.path.join(instance_dir, 'book_platform.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{default_db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session & Cookie Security (CTRL-01)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600))

    # CSRF Protection (CTRL-03)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Security Policy
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload
    STRICT_INPUT_VALIDATION = True

class TestConfig(Config):
    """Testing configuration with in-memory DB and disabled CSRF for targeted testing where specified."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key-for-local-pytest-only'
