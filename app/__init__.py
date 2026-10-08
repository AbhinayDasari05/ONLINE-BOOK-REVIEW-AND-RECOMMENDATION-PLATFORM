import os
from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager, csrf
from app.models.user import User

def create_app(config_class=Config):
    """Application factory for secure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Security Headers Middleware (CTRL-09)
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "frame-ancestors 'none';"
        )
        return response

    # Hardened Custom Error Handlers (CTRL-07, RULE I - No stack traces exposed)
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        # Database rollback on internal error
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.catalog import catalog_bp
    from app.routes.reviews import reviews_bp
    from app.routes.reading_list import reading_list_bp
    from app.routes.admin import admin_bp
    from app.routes.health import health_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(reading_list_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(health_bp)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()

    return app
