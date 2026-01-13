import os

class Config:
    """Base configuration class with default settings"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Flask-RESTx settings
    RESTX_MASK_SWAGGER = False
    ERROR_404_HELP = False
    
    # Application settings
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    # In production, SECRET_KEY must be set via environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
