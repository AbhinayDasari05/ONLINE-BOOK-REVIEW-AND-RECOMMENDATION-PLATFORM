from tests.conftest import login_client
from app.models.book import Book
from app.models.review import Review
from app.models.user import User

def test_user_b_cannot_edit_user_a_review(client, app):
    """
    TEST-05: Server-Side Object-Level Authorization Check (CTRL-02, Rule A).
    User A (Alice) creates a review.
    User B (Bob) attempts to modify Alice's review directly via POST /reviews/<id>/edit.
    Expected: Request denied, flash error displayed, review content in DB unchanged.
    """
    with app.app_context():
        book = Book.query.first()
        alice = User.query.filter_by(username="alice").first()
        
        # Alice creates a review
        alice_review = Review(
            book_id=book.id,
            user_id=alice.id,
            rating=5,
            content="Original legitimate review by Alice."
        )
        app.extensions['sqlalchemy'].session.add(alice_review)
        app.extensions['sqlalchemy'].session.commit()
        review_id = alice_review.id

    # Bob logs in
    login_client(client, "bob", "BobSecret123!")

    # Bob maliciously attempts to edit Alice's review
    malicious_resp = client.post(f'/reviews/{review_id}/edit', data={
        'rating': '1',
        'content': 'Malicious overwrite by Bob!'
    }, follow_redirects=True)

    # Verify authorization error message in response
    assert b"Access denied: You can only edit your own reviews" in malicious_resp.data

    # Verify database was NOT modified
    with app.app_context():
        persisted = Review.query.get(review_id)
        assert persisted.rating == 5
        assert persisted.content == "Original legitimate review by Alice."

def test_user_b_cannot_delete_user_a_review(client, app):
    """
    TEST-06: Server-Side Object-Level Authorization Check (CTRL-02, Rule A).
    User A (Alice) creates a review.
    User B (Bob) attempts to delete Alice's review directly via POST /reviews/<id>/delete.
    Expected: Request denied, flash error displayed, review remains intact in DB.
    """
    with app.app_context():
        book = Book.query.first()
        alice = User.query.filter_by(username="alice").first()

        alice_review = Review(
            book_id=book.id,
            user_id=alice.id,
            rating=4,
            content="Alice's permanent review."
        )
        app.extensions['sqlalchemy'].session.add(alice_review)
        app.extensions['sqlalchemy'].session.commit()
        review_id = alice_review.id

    # Bob logs in
    login_client(client, "bob", "BobSecret123!")

    # Bob attempts to delete Alice's review
    malicious_resp = client.post(f'/reviews/{review_id}/delete', follow_redirects=True)

    # Verify denial message
    assert b"Access denied: You can only delete your own reviews" in malicious_resp.data

    # Verify database still contains Alice's review
    with app.app_context():
        persisted = Review.query.get(review_id)
        assert persisted is not None
        assert persisted.content == "Alice's permanent review."

def test_normal_user_denied_admin_routes(client, app):
    """
    TEST-07: Role-Based Access Control (RBAC) (CTRL-06, Rule B).
    Normal user (Alice) attempts to access /admin/books and /admin/moderation.
    Expected: HTTP 403 Forbidden.
    """
    login_client(client, "alice", "AliceSecret123!")

    resp_books = client.get('/admin/books')
    assert resp_books.status_code == 403
    assert b"403" in resp_books.data

    resp_mod = client.get('/admin/moderation')
    assert resp_mod.status_code == 403
    assert b"403" in resp_mod.data

def test_admin_user_granted_admin_routes(client, app):
    """
    TEST-07b: RBAC verification for authorized administrator.
    Admin user logs in and accesses /admin/books.
    Expected: HTTP 200 OK.
    """
    login_client(client, "admin", "AdminSecret123!")

    resp_books = client.get('/admin/books')
    assert resp_books.status_code == 200
    assert b"Administrator: Book Catalog Management" in resp_books.data

    resp_mod = client.get('/admin/moderation')
    assert resp_mod.status_code == 200
    assert b"Content Moderation & Security Audit" in resp_mod.data

def test_anonymous_user_redirected_from_protected_routes(client, app):
    """
    TEST-08: Authentication Enforcement.
    Anonymous user tries to access /my-shelf and submit review.
    Expected: Redirect to /login.
    """
    resp_shelf = client.get('/my-shelf', follow_redirects=False)
    assert resp_shelf.status_code == 302
    assert '/login' in resp_shelf.headers['Location']

    resp_post = client.post('/books/1/reviews', data={'rating': '5', 'content': 'Test'}, follow_redirects=False)
    assert resp_post.status_code == 302
    assert '/login' in resp_post.headers['Location']
