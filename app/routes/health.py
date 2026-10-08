from flask import Blueprint, jsonify
from app.extensions import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint for Docker and Kubernetes liveness/readiness probes (DEP-03)."""
    try:
        # Verify database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "secure-book-review-platform"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": "database connection error"
        }), 503
