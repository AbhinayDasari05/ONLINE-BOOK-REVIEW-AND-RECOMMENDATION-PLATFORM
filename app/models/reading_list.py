from datetime import datetime
from app.extensions import db

VALID_STATUSES = ('want-to-read', 'reading', 'finished')

class ReadingListItem(db.Model):
    """Personal Reading List entity (COMP-06, REQ-09)."""
    __tablename__ = 'reading_list_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default='want-to-read')
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Unique constraint: each book can only appear once in a user's reading list
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book_reading_list'),
    )

    def is_owned_by(self, user) -> bool:
        """Object-level authorization check: reading list is private to the owner."""
        if not user or not user.is_authenticated:
            return False
        return self.user_id == user.id

    def __repr__(self):
        return f"<ReadingListItem User={self.user_id} Book={self.book_id} Status={self.status}>"
