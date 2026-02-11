# Flask app factory and extensions initialization

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Application factory pattern for Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.setdefault("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Create API and register namespaces
    api = Api(app, doc="/api/v1/docs", title="HBnB API", version="1.0",
              description="HBnB Application REST API")
    
    # Import and register namespaces inside function to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
    
    return app
