from tests.conftest import login_client
from app.models.book import Book
from app.models.review import Review

def test_xss_payload_in_review_is_autoescaped(client, app):
    """
    TEST-11 (Fuzzing/Security): Submit XSS payloads in review content.
    Verify that content is stored safely and rendered autoescaped (CTRL-04).
    """
    with app.app_context():
        book = Book.query.first()
        book_id = book.id

    login_client(client, "alice", "AliceSecret123!")

    xss_payload = "<script>alert('pwned')</script><img src='x' onerror='alert(1)'>"

    resp = client.post(f'/books/{book_id}/reviews', data={
        'rating': '4',
        'content': xss_payload
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Review submitted successfully" in resp.data

    # Retrieve page and verify raw script tag is NOT rendered executable
    detail_resp = client.get(f'/books/{book_id}')
    assert b"<script>alert('pwned')</script>" not in detail_resp.data
    # Safe HTML entities should be present
    assert b"&lt;script&gt;alert(&#39;pwned&#39;)&lt;/script&gt;" in detail_resp.data or b"&lt;script&gt;" in detail_resp.data

def test_rating_boundary_fuzzing(client, app):
    """TEST-11 (Fuzzing): Submit boundary and malformed ratings."""
    with app.app_context():
        book = Book.query.first()
        book_id = book.id

    login_client(client, "alice", "AliceSecret123!")

    bad_ratings = ['-1', '0', '6', '999999', 'abc', 'NaN', '3.5', 'null']
    for bad_r in bad_ratings:
        resp = client.post(f'/books/{book_id}/reviews', data={
            'rating': bad_r,
            'content': 'Valid length content for review testing.'
        }, follow_redirects=True)
        assert b"Rating must be an integer between 1 and 5" in resp.data

def test_sql_injection_search_fuzzing(client, app):
    """TEST-11 (Fuzzing): Fuzz search query with SQL injection patterns."""
    sqli_vectors = [
        "' OR '1'='1",
        "'; DROP TABLE books; --",
        "1' UNION SELECT id, username, email, password_hash, 1, 1 FROM users --",
        "' OR SLEEP(5) --",
        "\" or 1=1--"
    ]
    for vector in sqli_vectors:
        resp = client.get(f'/books?q={vector}')
        assert resp.status_code == 200
        # Check no database error or raw exception string
        assert b"OperationalError" not in resp.data
        assert b"syntax error" not in resp.data

def test_invalid_resource_ids(client, app):
    """TEST-11: Access invalid and non-existent IDs."""
    resp_404 = client.get('/books/9999999')
    assert resp_404.status_code == 404
    assert b"404" in resp_404.data

    resp_str = client.get('/books/not-a-number')
    assert resp_str.status_code == 404
