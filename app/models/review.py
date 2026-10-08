from datetime import datetime
from app.extensions import db

class Review(db.Model):
    """Review and Rating entity (COMP-05)."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # Validated 1 to 5 (REQ-05)
    content = db.Column(db.Text, nullable=False)    # Validated length bounds (REQ-06)
    
    # Moderation flags (REQ-11)
    is_moderated = db.Column(db.Boolean, default=False, nullable=False)
    moderation_reason = db.Column(db.String(255), nullable=True)
    moderated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    moderator = db.relationship('User', foreign_keys=[moderated_by], backref='moderated_reviews')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Unique constraint: exactly one review & rating per user per book (REQ-05)
    __table_args__ = (
        db.UniqueConstraint('book_id', 'user_id', name='uq_user_book_review'),
    )

    def is_owned_by(self, user) -> bool:
        """Object-level authorization check: verify user ownership (CTRL-02, REQ-07, REQ-08)."""
        if not user or not user.is_authenticated:
            return False
        return self.user_id == user.id

    def __repr__(self):
        return f"<Review {self.id} on Book {self.book_id} by User {self.user_id} (Rating: {self.rating})>"
