from tests.conftest import login_client

def test_user_registration_integration(client, app):
    """TEST-04: Complete user registration workflow via HTTP POST."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPassword123!',
        'confirm_password': 'StrongPassword123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registration successful" in response.data

def test_login_and_logout_session_invalidation(client, app):
    """TEST-04: Test login, authenticated session cookie, and server-side logout invalidation (REQ-12)."""
    # 1. Login with valid credentials
    resp = login_client(client, "alice", "AliceSecret123!")
    assert resp.status_code == 200
    assert b"Welcome back, alice!" in resp.data

    # 2. Access protected endpoint (My Shelf)
    shelf_resp = client.get('/my-shelf')
    assert shelf_resp.status_code == 200
    assert b"My Personal Reading Shelf" in shelf_resp.data

    # 3. Perform logout
    logout_resp = client.get('/logout', follow_redirects=True)
    assert logout_resp.status_code == 200
    assert b"You have been securely logged out" in logout_resp.data

    # 4. Verify protected shelf is no longer accessible without logging back in
    shelf_after = client.get('/my-shelf', follow_redirects=True)
    assert b"Please log in to access this page" in shelf_after.data
