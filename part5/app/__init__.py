"""
HBnB V2 — Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_name='development'):
    """Create and configure the Flask application"""
    from config import config

    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    app.config.from_object(config.get(config_name, config['default']))

    # Ensure directories exist
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True)

    # Register API blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Register frontend routes
    from app.routes import frontend
    app.register_blueprint(frontend)

    # Create tables
    with app.app_context():
        from app.models import user, place, booking, payment, review, amenity, media, city, otp, site_settings
        db.create_all()

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"error": "Token has expired", "error_ar": "انتهت صلاحية الرمز"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"error": "Invalid token", "error_ar": "رمز غير صالح"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"error": "Authorization required", "error_ar": "التفويض مطلوب"}, 401

    return app
