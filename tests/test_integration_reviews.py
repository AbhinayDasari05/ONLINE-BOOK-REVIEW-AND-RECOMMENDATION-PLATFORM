from tests.conftest import login_client
from app.models.book import Book
from app.models.review import Review

def test_full_review_lifecycle(client, app):
    """TEST-09: Complete review creation, persistence, aggregation, and retrieval integration."""
    with app.app_context():
        book = Book.query.first()
        book_id = book.id

    # Alice logs in
    login_client(client, "alice", "AliceSecret123!")

    # Alice submits a 5-star review
    post_resp = client.post(f'/books/{book_id}/reviews', data={
        'rating': '5',
        'content': 'Outstanding guide to secure software lifecycle and defense-in-depth.'
    }, follow_redirects=True)

    assert post_resp.status_code == 200
    assert b"Review submitted successfully" in post_resp.data

    # Verify review persisted in DB
    with app.app_context():
        rev = Review.query.filter_by(book_id=book_id).first()
        assert rev is not None
        assert rev.rating == 5
        assert "Outstanding guide" in rev.content

        # Verify average rating updated on book
        book_updated = Book.query.get(book_id)
        assert book_updated.average_rating == 5.0
        assert book_updated.review_count == 1

    # Verify review appears on the public book detail screen
    detail_resp = client.get(f'/books/{book_id}')
    assert detail_resp.status_code == 200
    assert b"Outstanding guide to secure software lifecycle" in detail_resp.data
    assert b"alice" in detail_resp.data
