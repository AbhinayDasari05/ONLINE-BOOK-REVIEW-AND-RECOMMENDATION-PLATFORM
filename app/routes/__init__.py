from app.routes.auth import auth_bp
from app.routes.catalog import catalog_bp
from app.routes.reviews import reviews_bp
from app.routes.reading_list import reading_list_bp
from app.routes.admin import admin_bp
from app.routes.health import health_bp

__all__ = ['auth_bp', 'catalog_bp', 'reviews_bp', 'reading_list_bp', 'admin_bp', 'health_bp']
