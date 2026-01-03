from app.routes.auth import auth_bp
from app.routes.api import api_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
