"""Main Flask Application Entry Point"""
from flask import Flask
from app.api import api
from app.services.facade import HBnBFacade


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure the app
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False
    
    # Initialize the API
    api.init_app(app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
