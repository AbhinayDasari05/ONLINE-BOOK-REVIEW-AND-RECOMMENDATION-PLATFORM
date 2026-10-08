from app.models.book import Book
from app.core.security import sanitize_text

class SearchService:
    """Secure Book Search Subsystem using parameterized ORM queries (COMP-04, REQ-03, CTRL-05)."""

    @staticmethod
    def search_books(query: str = "", genre: str = "", author: str = "", limit: int = 50):
        """
        Execute parameterized search against Book catalog.
        Protects against SQL injection by using SQLAlchemy ORM filter constructs with bound parameters.
        """
        stmt = Book.query

        if query:
            cleaned_query = sanitize_text(query, 100)
            pattern = f"%{cleaned_query}%"
            stmt = stmt.filter(
                (Book.title.ilike(pattern)) | 
                (Book.description.ilike(pattern)) |
                (Book.author.ilike(pattern))
            )

        if author:
            cleaned_author = sanitize_text(author, 100)
            stmt = stmt.filter(Book.author.ilike(f"%{cleaned_author}%"))

        if genre:
            cleaned_genre = sanitize_text(genre, 80)
            if cleaned_genre.lower() != 'all':
                stmt = stmt.filter(Book.genre.ilike(f"%{cleaned_genre}%"))

        return stmt.order_by(Book.title.asc()).limit(limit).all()

    @staticmethod
    def get_all_genres() -> list[str]:
        """Fetch distinct genres for search filtering."""
        results = Book.query.with_entities(Book.genre).distinct().all()
        return sorted([r[0] for r in results if r[0]])
