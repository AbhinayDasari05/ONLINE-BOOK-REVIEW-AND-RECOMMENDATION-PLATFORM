from app.extensions import db
from app.models.review import Review
from app.models.book import Book
from app.core.security import validate_rating, sanitize_text
from app.core.audit import log_audit_event

class ReviewService:
    """Review and Rating service with strict server-side authorization (COMP-05, CTRL-02, REQ-05..08, REQ-11)."""

    @staticmethod
    def get_reviews_for_book(book_id: int, include_moderated: bool = False):
        """Retrieve reviews for a book; filters out moderated reviews unless requested by admin."""
        stmt = Review.query.filter_by(book_id=book_id)
        if not include_moderated:
            stmt = stmt.filter_by(is_moderated=False)
        return stmt.order_by(Review.created_at.desc()).all()

    @staticmethod
    def get_review_by_id(review_id: int) -> Review or None:
        """Fetch review by primary key."""
        return Review.query.get(review_id)

    @staticmethod
    def create_review(user, book_id: int, rating: int, content: str) -> tuple[bool, str, Review or None]:
        """
        Submit a new rating and review (REQ-05, REQ-06).
        Enforces:
        - 1 rating per user per book
        - rating between 1 and 5
        - review content length bounds
        """
        if not user or not user.is_authenticated:
            return False, "Authentication required to submit reviews.", None

        book = Book.query.get(book_id)
        if not book:
            return False, "Specified book does not exist.", None

        valid_r, parsed_rating = validate_rating(rating)
        if not valid_r:
            return False, "Rating must be an integer between 1 and 5.", None

        cleaned_content = sanitize_text(content, 2000)
        if not cleaned_content or len(cleaned_content) < 5:
            return False, "Review content must be at least 5 characters long.", None

        # Check existing review for this user and book
        existing_review = Review.query.filter_by(user_id=user.id, book_id=book_id).first()
        if existing_review:
            return False, "You have already reviewed this book. You may edit your existing review instead.", None

        try:
            review = Review(
                user_id=user.id,
                book_id=book_id,
                rating=parsed_rating,
                content=cleaned_content
            )
            db.session.add(review)
            db.session.commit()

            log_audit_event("REVIEW_CREATED", "Review", review.id, "SUCCESS", f"User {user.username} rated book {book_id} with {parsed_rating}")
            return True, "Review submitted successfully.", review
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to submit review: {str(e)}", None

    @staticmethod
    def update_review(user, review_id: int, rating: int, content: str) -> tuple[bool, str, Review or None]:
        """
        Update an existing review (REQ-07, CTRL-02).
        CRITICAL SECURITY CHECK:
        Server-side object-level authorization: current user MUST be the review owner.
        """
        review = Review.query.get(review_id)
        if not review:
            return False, "Review not found.", None

        # Server-side Object-Level Authorization Check (CTRL-02, Rule A)
        if not review.is_owned_by(user):
            log_audit_event("UNAUTHORIZED_REVIEW_EDIT_ATTEMPT", "Review", review_id, "DENIED",
                            f"User {getattr(user, 'username', 'anon')} attempted to edit review owned by User {review.user_id}")
            return False, "Access denied: You can only edit your own reviews.", None

        valid_r, parsed_rating = validate_rating(rating)
        if not valid_r:
            return False, "Rating must be an integer between 1 and 5.", None

        cleaned_content = sanitize_text(content, 2000)
        if not cleaned_content or len(cleaned_content) < 5:
            return False, "Review content must be at least 5 characters long.", None

        try:
            review.rating = parsed_rating
            review.content = cleaned_content
            # If a review was previously moderated, editing puts it back into review or resets flags
            db.session.commit()

            log_audit_event("REVIEW_UPDATED", "Review", review.id, "SUCCESS", f"User {user.username} updated review {review.id}")
            return True, "Review updated successfully.", review
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update review: {str(e)}", None

    @staticmethod
    def delete_review(user, review_id: int) -> tuple[bool, str]:
        """
        Delete a review (REQ-08, CTRL-02).
        CRITICAL SECURITY CHECK:
        Server-side object-level authorization: current user MUST be the review owner.
        (Admins may moderate/hide, but ordinary deletion is reserved for the author).
        """
        review = Review.query.get(review_id)
        if not review:
            return False, "Review not found."

        # Server-side Object-Level Authorization Check (CTRL-02, Rule A)
        if not review.is_owned_by(user) and not getattr(user, 'is_admin', False):
            log_audit_event("UNAUTHORIZED_REVIEW_DELETE_ATTEMPT", "Review", review_id, "DENIED",
                            f"User {getattr(user, 'username', 'anon')} attempted to delete review owned by User {review.user_id}")
            return False, "Access denied: You can only delete your own reviews."

        try:
            db.session.delete(review)
            db.session.commit()

            log_audit_event("REVIEW_DELETED", "Review", review_id, "SUCCESS", f"User {getattr(user, 'username', 'unknown')} deleted review {review_id}")
            return True, "Review deleted successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete review: {str(e)}"

    @staticmethod
    def moderate_review(admin_user, review_id: int, hide: bool, reason: str) -> tuple[bool, str, Review or None]:
        """
        Administrator moderates an inappropriate review (REQ-11, CTRL-06).
        Records moderation reason and generates tamper-evident audit record.
        """
        if not admin_user or not getattr(admin_user, 'is_admin', False):
            log_audit_event("UNAUTHORIZED_MODERATION_ATTEMPT", "Review", review_id, "DENIED", "Non-admin attempted moderation")
            return False, "Access denied: Administrator privileges required.", None

        review = Review.query.get(review_id)
        if not review:
            return False, "Review not found.", None

        cleaned_reason = sanitize_text(reason, 255)
        if hide and not cleaned_reason:
            return False, "A moderation reason is required when hiding a review.", None

        try:
            review.is_moderated = hide
            review.moderation_reason = cleaned_reason if hide else None
            review.moderated_by = admin_user.id
            db.session.commit()

            action = "REVIEW_HIDDEN" if hide else "REVIEW_RESTORED"
            log_audit_event(action, "Review", review.id, "SUCCESS", f"Admin {admin_user.username} moderated review {review.id}: {cleaned_reason}")
            return True, f"Review has been {'moderated and hidden' if hide else 'restored'}.", review
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to moderate review: {str(e)}", None
