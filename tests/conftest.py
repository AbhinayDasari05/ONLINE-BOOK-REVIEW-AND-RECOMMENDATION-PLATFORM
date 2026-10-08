import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models.user import User
from app.models.book import Book
from app.models.review import Review
from app.models.reading_list import ReadingListItem

@pytest.fixture
def app():
    """Create isolated test application with in-memory SQLite database."""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        # Seed standard test users
        admin = User(username="admin", email="admin@test.local", is_admin=True)
        admin.set_password("AdminSecret123!")

        alice = User(username="alice", email="alice@test.local", is_admin=False)
        alice.set_password("AliceSecret123!")

        bob = User(username="bob", email="bob@test.local", is_admin=False)
        bob.set_password("BobSecret123!")

        db.session.add_all([admin, alice, bob])

        # Seed test book
        book1 = Book(
            title="Secure Software Engineering Fundamentals",
            author="Dr. Alice Vance",
            genre="Cybersecurity",
            isbn="978-0111111111",
            description="Foundational principles of secure programming and verification.",
            publication_year=2024
        )
        book2 = Book(
            title="Advanced DevSecOps Architecture",
            author="Bob Ross",
            genre="DevOps",
            isbn="978-0222222222",
            description="Automating security pipelines in continuous delivery environments.",
            publication_year=2023
        )
        db.session.add_all([book1, book2])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()

def login_client(client, username_or_email, password):
    """Helper to authenticate client session."""
    return client.post('/login', data={
        'username_or_email': username_or_email,
        'password': password
    }, follow_redirects=True)
