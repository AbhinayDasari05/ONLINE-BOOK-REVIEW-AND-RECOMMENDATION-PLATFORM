from app.services.search_service import SearchService

def test_search_by_title_and_keyword(app):
    """TEST-03: Test parameterized search by title keyword."""
    with app.app_context():
        results = SearchService.search_books(query="Fundamentals")
        assert len(results) == 1
        assert "Fundamentals" in results[0].title

def test_search_by_genre(app):
    """TEST-03: Test parameterized search by genre."""
    with app.app_context():
        results = SearchService.search_books(genre="Cybersecurity")
        assert len(results) == 1
        assert results[0].genre == "Cybersecurity"

def test_search_sql_injection_metacharacters(app):
    """TEST-03: Verify SQL injection payloads do not break ORM query or leak data."""
    with app.app_context():
        # Classical SQL injection string
        results = SearchService.search_books(query="' OR 1=1 --")
        # Should execute safely as literal text search and return 0 matches
        assert len(results) == 0

        # Blind SQL injection string
        results2 = SearchService.search_books(query="'; DROP TABLE books; --")
        assert len(results2) == 0
