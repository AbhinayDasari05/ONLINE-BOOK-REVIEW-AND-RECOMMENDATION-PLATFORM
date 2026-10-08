from datetime import datetime
from app.extensions import db

class Book(db.Model):
    """Book catalog entity (COMP-03)."""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(150), nullable=False, index=True)
    genre = db.Column(db.String(80), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    reading_list_entries = db.relationship('ReadingListItem', backref='book', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def average_rating(self) -> float:
        """Calculate average rating excluding hidden/moderated reviews."""
        active_reviews = self.reviews.filter_by(is_moderated=False).all()
        if not active_reviews:
            return 0.0
        return round(sum(r.rating for r in active_reviews) / len(active_reviews), 2)

    @property
    def review_count(self) -> int:
        """Count of active published reviews."""
        return self.reviews.filter_by(is_moderated=False).count()

    def __repr__(self):
        return f"<Book '{self.title}' by {self.author}>"
