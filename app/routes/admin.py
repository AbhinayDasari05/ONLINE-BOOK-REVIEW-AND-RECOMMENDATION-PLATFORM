from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.core.security import admin_required
from app.services.book_service import BookService
from app.services.review_service import ReviewService
from app.models.review import Review
from app.models.audit_log import AuditLog

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_bp.route('/books')
@login_required
@admin_required
def books():
    """Admin book management dashboard (REQ-10)."""
    all_books = BookService.get_all_books(limit=100)
    return render_template('admin/books.html', books=all_books)

@admin_bp.route('/books/new', methods=['POST'])
@login_required
@admin_required
def add_book():
    """Admin creates a new book in catalog (REQ-10)."""
    title = request.form.get('title', '')
    author = request.form.get('author', '')
    genre = request.form.get('genre', '')
    isbn = request.form.get('isbn', '')
    description = request.form.get('description', '')
    year = request.form.get('publication_year', 0)

    success, message, _ = BookService.create_book(title, author, genre, isbn, description, year)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('admin.books'))

@admin_bp.route('/books/<int:book_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_book(book_id: int):
    """Admin updates book details (REQ-10)."""
    title = request.form.get('title', '')
    author = request.form.get('author', '')
    genre = request.form.get('genre', '')
    isbn = request.form.get('isbn', '')
    description = request.form.get('description', '')
    year = request.form.get('publication_year', 0)

    success, message, _ = BookService.update_book(book_id, title, author, genre, isbn, description, year)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('admin.books'))

@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id: int):
    """Admin deletes book from catalog (REQ-10)."""
    success, message = BookService.delete_book(book_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('admin.books'))

@admin_bp.route('/moderation')
@login_required
@admin_required
def moderation():
    """Admin review moderation dashboard (REQ-11)."""
    reviews = Review.query.order_by(Review.created_at.desc()).limit(100).all()
    audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(50).all()
    return render_template('admin/moderation.html', reviews=reviews, audit_logs=audit_logs)

@admin_bp.route('/reviews/<int:review_id>/moderate', methods=['POST'])
@login_required
@admin_required
def moderate_review(review_id: int):
    """Admin hides or un-hides a review with reason (REQ-11)."""
    hide = request.form.get('action') == 'hide'
    reason = request.form.get('reason', '').strip()

    success, message, _ = ReviewService.moderate_review(
        admin_user=current_user,
        review_id=review_id,
        hide=hide,
        reason=reason
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('admin.moderation'))
