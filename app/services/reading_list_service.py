from app.extensions import db
from app.models.reading_list import ReadingListItem, VALID_STATUSES
from app.models.book import Book
from app.core.audit import log_audit_event

class ReadingListService:
    """Personal Reading List management service (COMP-06, REQ-09)."""

    @staticmethod
    def get_user_reading_list(user):
        """Fetch reading list for authenticated user. Privacy enforced."""
        if not user or not user.is_authenticated:
            return []
        return ReadingListItem.query.filter_by(user_id=user.id).order_by(ReadingListItem.updated_at.desc()).all()

    @staticmethod
    def add_or_update_book(user, book_id: int, status: str = 'want-to-read') -> tuple[bool, str, ReadingListItem or None]:
        """Add a book to reading list or update its reading status."""
        if not user or not user.is_authenticated:
            return False, "Authentication required to manage reading lists.", None

        if status not in VALID_STATUSES:
            return False, f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}", None

        book = Book.query.get(book_id)
        if not book:
            return False, "Book does not exist.", None

        item = ReadingListItem.query.filter_by(user_id=user.id, book_id=book_id).first()
        try:
            if item:
                item.status = status
                action = "READING_LIST_UPDATED"
            else:
                item = ReadingListItem(
                    user_id=user.id,
                    book_id=book_id,
                    status=status
                )
                db.session.add(item)
                action = "READING_LIST_ADDED"

            db.session.commit()
            log_audit_event(action, "ReadingListItem", item.id, "SUCCESS", f"User {user.username} set book {book_id} to {status}")
            return True, f"Book status updated to '{status}'.", item
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update reading list: {str(e)}", None

    @staticmethod
    def remove_book(user, item_id: int) -> tuple[bool, str]:
        """Remove book from personal reading list (Object authorization: owner only)."""
        if not user or not user.is_authenticated:
            return False, "Authentication required."

        item = ReadingListItem.query.get(item_id)
        if not item:
            return False, "Reading list entry not found."

        if not item.is_owned_by(user):
            log_audit_event("UNAUTHORIZED_READING_LIST_ACCESS", "ReadingListItem", item_id, "DENIED",
                            f"User {user.username} attempted to remove item owned by User {item.user_id}")
            return False, "Access denied: You can only modify your own reading list."

        try:
            db.session.delete(item)
            db.session.commit()
            log_audit_event("READING_LIST_REMOVED", "ReadingListItem", item_id, "SUCCESS", f"User {user.username} removed item {item_id}")
            return True, "Book removed from your reading list."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to remove item: {str(e)}"
