from app.core.security import validate_rating, sanitize_text

def test_rating_valid_boundaries():
    """TEST-02: Test valid integer ratings 1 to 5."""
    for r in [1, 2, 3, 4, 5]:
        valid, val = validate_rating(r)
        assert valid is True
        assert val == r

def test_rating_invalid_boundaries():
    """TEST-02: Test ratings outside 1-5 or malformed types."""
    # Out of range integers
    assert validate_rating(0)[0] is False
    assert validate_rating(6)[0] is False
    assert validate_rating(-1)[0] is False
    assert validate_rating(100)[0] is False

    # Non-integers / invalid types
    assert validate_rating("five")[0] is False
    assert validate_rating(None)[0] is False
    assert validate_rating("<script>alert(1)</script>")[0] is False

def test_text_sanitization():
    """Test text trimmer and null-byte stripper."""
    raw = "  Hello World!\x00  "
    cleaned = sanitize_text(raw, 50)
    assert cleaned == "Hello World!"
    assert '\x00' not in cleaned
