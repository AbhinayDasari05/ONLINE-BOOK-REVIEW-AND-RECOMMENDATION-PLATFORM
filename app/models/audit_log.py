from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    """Tamper-evident Security Audit Log entity (COMP-08, CTRL-08)."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    username = db.Column(db.String(50), nullable=True)
    action = db.Column(db.String(80), nullable=False, index=True)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.String(50), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    status = db.Column(db.String(20), nullable=False)  # SUCCESS, FAILURE, DENIED
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<AuditLog [{self.timestamp}] Action={self.action} User={self.username} Status={self.status}>"
