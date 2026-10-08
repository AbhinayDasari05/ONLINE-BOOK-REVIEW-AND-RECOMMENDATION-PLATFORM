from tests.conftest import login_client
from app.models.book import Book
from app.models.reading_list import ReadingListItem
from app.models.review import Review

def test_complete_end_to_end_user_journey(client, app):
    """
    TEST-10: End-to-End System Workflow Test.
    Journey: Register -> Login -> Search -> Detail -> Shelf Add -> Review -> Shelf Verify -> Logout.
    """
    # 1. Register new user
    reg_resp = client.post('/register', data={
        'username': 'david',
        'email': 'david@platform.local',
        'password': 'DavidSecret2026!',
        'confirm_password': 'DavidSecret2026!'
    }, follow_redirects=True)
    assert reg_resp.status_code == 200
    assert b"Registration successful" in reg_resp.data

    # 2. Login as David
    login_resp = login_client(client, "david", "DavidSecret2026!")
    assert login_resp.status_code == 200
    assert b"Welcome back, david!" in login_resp.data

    # 3. Search books
    search_resp = client.get('/books?q=Fundamentals')
    assert search_resp.status_code == 200
    assert b"Secure Software Engineering Fundamentals" in search_resp.data

    with app.app_context():
        book = Book.query.filter_by(title="Secure Software Engineering Fundamentals").first()
        book_id = book.id

    # 4. View Book Details
    detail_resp = client.get(f'/books/{book_id}')
    assert detail_resp.status_code == 200
    assert b"Leave a Review" in detail_resp.data

    # 5. Add to Reading Shelf
    shelf_add = client.post('/reading-list/add', data={
        'book_id': str(book_id),
        'status': 'want-to-read'
    }, follow_redirects=True)
    assert shelf_add.status_code == 200
    assert b"want-to-read" in shelf_add.data

    # 6. Post Rating and Review
    review_post = client.post(f'/books/{book_id}/reviews', data={
        'rating': '5',
        'content': 'An exceptional resource for secure design principles!'
    }, follow_redirects=True)
    assert review_post.status_code == 200
    assert b"Review submitted successfully" in review_post.data

    # 7. Visit My Shelf
    my_shelf = client.get('/my-shelf')
    assert my_shelf.status_code == 200
    assert b"Secure Software Engineering Fundamentals" in my_shelf.data
    assert b"An exceptional resource for secure design principles!" in my_shelf.data

    # 8. Update Shelf Status to 'finished'
    shelf_update = client.post('/reading-list/add', data={
        'book_id': str(book_id),
        'status': 'finished'
    }, follow_redirects=True)
    assert shelf_update.status_code == 200
    assert b"finished" in shelf_update.data

    # 9. Log out
    logout_resp = client.get('/logout', follow_redirects=True)
    assert logout_resp.status_code == 200
    assert b"You have been securely logged out" in logout_resp.data
