from flask import Blueprint, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.services.review_service import ReviewService

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/books/<int:book_id>/reviews', methods=['POST'])
@login_required
def add_review(book_id: int):
    """Submit a rating and review (REQ-05, REQ-06)."""
    rating = request.form.get('rating')
    content = request.form.get('content', '')

    success, message, review = ReviewService.create_review(
        user=current_user,
        book_id=book_id,
        rating=rating,
        content=content
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for('catalog.detail', book_id=book_id))

@reviews_bp.route('/reviews/<int:review_id>/edit', methods=['POST'])
@login_required
def edit_review(review_id: int):
    """
    Edit own review (REQ-07).
    Enforces server-side object-level authorization: User B cannot edit User A's review.
    """
    review = ReviewService.get_review_by_id(review_id)
    if not review:
        abort(404)

    book_id = review.book_id
    rating = request.form.get('rating')
    content = request.form.get('content', '')

    success, message, _ = ReviewService.update_review(
        user=current_user,
        review_id=review_id,
        rating=rating,
        content=content
    )

    if success:
        flash(message, "success")
    else:
        # Access denied or validation failure
        flash(message, "danger")

    return redirect(url_for('catalog.detail', book_id=book_id))

@reviews_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id: int):
    """
    Delete own review (REQ-08).
    Enforces server-side object-level authorization: User B cannot delete User A's review.
    """
    review = ReviewService.get_review_by_id(review_id)
    if not review:
        abort(404)

    book_id = review.book_id
    success, message = ReviewService.delete_review(
        user=current_user,
        review_id=review_id
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for('catalog.detail', book_id=book_id))
