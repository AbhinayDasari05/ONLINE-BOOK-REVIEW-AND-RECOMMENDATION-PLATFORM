from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.reading_list_service import ReadingListService
from app.models.review import Review

reading_list_bp = Blueprint('reading_list', __name__)

@reading_list_bp.route('/my-shelf')
@login_required
def index():
    """Display user's private reading list and their submitted reviews (REQ-09)."""
    items = ReadingListService.get_user_reading_list(current_user)
    my_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template('reading_list/index.html', items=items, my_reviews=my_reviews)

@reading_list_bp.route('/reading-list/add', methods=['POST'])
@login_required
def add_or_update():
    """Add a book to reading list or update its status."""
    book_id = request.form.get('book_id')
    status = request.form.get('status', 'want-to-read')

    try:
        book_id_int = int(book_id)
    except (ValueError, TypeError):
        flash("Invalid book specified.", "danger")
        return redirect(url_for('catalog.index'))

    success, message, _ = ReadingListService.add_or_update_book(
        user=current_user,
        book_id=book_id_int,
        status=status
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(request.referrer or url_for('reading_list.index'))

@reading_list_bp.route('/reading-list/<int:item_id>/delete', methods=['POST'])
@login_required
def remove(item_id: int):
    """Remove a book from reading list with ownership authorization."""
    success, message = ReadingListService.remove_book(current_user, item_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('reading_list.index'))
