from app.extensions import db
from app.models.book import Book
from app.core.security import sanitize_text
from app.core.audit import log_audit_event

class BookService:
    """Book catalog management service (COMP-03, REQ-04, REQ-10)."""

    @staticmethod
    def get_all_books(limit: int = 50, offset: int = 0):
        """Retrieve paginated book catalog."""
        return Book.query.order_by(Book.title.asc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_book_by_id(book_id: int) -> Book or None:
        """Retrieve single book by ID."""
        return Book.query.get(book_id)

    @staticmethod
    def create_book(title: str, author: str, genre: str, isbn: str, description: str, publication_year: int) -> tuple[bool, str, Book or None]:
        """Admin creates a new book record (REQ-10)."""
        title = sanitize_text(title, 200)
        author = sanitize_text(author, 150)
        genre = sanitize_text(genre, 80)
        isbn = sanitize_text(isbn, 20)
        description = sanitize_text(description, 5000)

        if not title or not author or not genre or not isbn or not description:
            return False, "All book fields are required.", None

        try:
            year = int(publication_year)
            if year < 1000 or year > 2100:
                return False, "Publication year must be between 1000 and 2100.", None
        except (ValueError, TypeError):
            return False, "Invalid publication year.", None

        if Book.query.filter_by(isbn=isbn).first():
            return False, f"Book with ISBN '{isbn}' already exists.", None

        try:
            book = Book(
                title=title,
                author=author,
                genre=genre,
                isbn=isbn,
                description=description,
                publication_year=year
            )
            db.session.add(book)
            db.session.commit()

            log_audit_event("BOOK_CREATED", "Book", book.id, "SUCCESS", f"Created book: {title} ({isbn})")
            return True, "Book created successfully.", book
        except Exception as e:
            db.session.rollback()
            return False, f"Error saving book: {str(e)}", None

    @staticmethod
    def update_book(book_id: int, title: str, author: str, genre: str, isbn: str, description: str, publication_year: int) -> tuple[bool, str, Book or None]:
        """Admin updates an existing book record (REQ-10)."""
        book = Book.query.get(book_id)
        if not book:
            return False, "Book not found.", None

        title = sanitize_text(title, 200)
        author = sanitize_text(author, 150)
        genre = sanitize_text(genre, 80)
        isbn = sanitize_text(isbn, 20)
        description = sanitize_text(description, 5000)

        if not title or not author or not genre or not isbn or not description:
            return False, "All fields are required.", None

        try:
            year = int(publication_year)
        except (ValueError, TypeError):
            return False, "Invalid publication year.", None

        # Check ISBN uniqueness if changed
        existing_isbn = Book.query.filter(Book.isbn == isbn, Book.id != book_id).first()
        if existing_isbn:
            return False, f"ISBN '{isbn}' is already used by another book.", None

        try:
            book.title = title
            book.author = author
            book.genre = genre
            book.isbn = isbn
            book.description = description
            book.publication_year = year
            db.session.commit()

            log_audit_event("BOOK_UPDATED", "Book", book.id, "SUCCESS", f"Updated book {book.id}: {title}")
            return True, "Book updated successfully.", book
        except Exception as e:
            db.session.rollback()
            return False, f"Error updating book: {str(e)}", None

    @staticmethod
    def delete_book(book_id: int) -> tuple[bool, str]:
        """Admin deletes a book record (REQ-10)."""
        book = Book.query.get(book_id)
        if not book:
            return False, "Book not found."

        try:
            title = book.title
            db.session.delete(book)
            db.session.commit()

            log_audit_event("BOOK_DELETED", "Book", book_id, "SUCCESS", f"Deleted book {book_id}: {title}")
            return True, "Book deleted successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting book: {str(e)}"
