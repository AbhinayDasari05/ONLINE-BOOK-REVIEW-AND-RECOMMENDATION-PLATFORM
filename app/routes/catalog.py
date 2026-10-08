from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from app.services.book_service import BookService
from app.services.search_service import SearchService
from app.services.review_service import ReviewService
from app.models.reading_list import ReadingListItem
from app.models.review import Review

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/')
@catalog_bp.route('/books')
def index():
    """Book discovery and search screen (REQ-03)."""
    q = request.args.get('q', '').strip()
    genre = request.args.get('genre', '').strip()
    author = request.args.get('author', '').strip()

    if q or genre or author:
        books = SearchService.search_books(query=q, genre=genre, author=author)
    else:
        books = BookService.get_all_books()

    all_books = BookService.get_all_books()
    genres = SearchService.get_all_genres()
    total_reviews = Review.query.count()

    return render_template(
        'catalog/search.html',
        books=books,
        genres=genres,
        q=q,
        selected_genre=genre,
        author=author,
        total_books=len(all_books),
        total_reviews=total_reviews
    )


@catalog_bp.route('/books/<int:book_id>')
def detail(book_id: int):
    """Book detail view with ratings and review thread (REQ-04)."""
    book = BookService.get_book_by_id(book_id)
    if not book:
        abort(404)

    reviews = ReviewService.get_reviews_for_book(book_id)
    user_review = None
    reading_list_status = None

    if current_user.is_authenticated:
        for r in reviews:
            if r.user_id == current_user.id:
                user_review = r
                break
        rl_item = ReadingListItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if rl_item:
            reading_list_status = rl_item.status

    return render_template(
        'catalog/detail.html',
        book=book,
        reviews=reviews,
        user_review=user_review,
        reading_list_status=reading_list_status
    )
