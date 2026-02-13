"""
HBnB V2 — Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'hbnb-v2-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'hbnb-v2-jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Resend Email
    RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'noreply@rizi.app')

    # Offline Payment — Bank Details
    BANK_NAME = os.getenv('BANK_NAME', 'الراجحي — Al Rajhi Bank')
    BANK_IBAN = os.getenv('BANK_IBAN', 'SA00 8000 0000 0000 12346 7519')
    ACCOUNT_HOLDER = os.getenv('ACCOUNT_HOLDER', 'Rizi Platform')

    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyDKXY_py-Ku0hm_EKZAYV5A86PTpzdNSSY')

    # Media Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    # Localization
    DEFAULT_LANGUAGE = 'ar'
    SUPPORTED_LANGUAGES = ['ar', 'en']
    DEFAULT_COUNTRY = 'SA'

    # OTP Settings
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    MAGIC_LINK_EXPIRY_MINUTES = 30

    # Privacy
    PRIVACY_RADIUS_MILES = 500

    # Monthly discount
    MONTHLY_DISCOUNT_PERCENT = 10

    # Booking rules
    CHECK_IN_TIME = '16:00'   # 4:00 PM
    CHECK_OUT_TIME = '12:00'  # 12:00 PM (noon)
    CLEANING_HOURS = 4        # 4 hours between guests

    # App identity
    APP_NAME = 'Rizi'
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
    DOMAIN = os.getenv('DOMAIN', 'rizi.app')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'hbnb_v2.db')
    )


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    APP_URL = os.getenv('APP_URL', 'https://rizi.app')

    # Tighter security in production
    JWT_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
