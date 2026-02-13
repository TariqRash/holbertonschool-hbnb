"""
HBnB V2 — OTP & Magic Link Model
Passwordless authentication tokens.
"""
from app import db
from app.models.base_model import BaseModel
from datetime import datetime, timedelta, timezone
import secrets
import string


class OTP(BaseModel):
    """One-Time Password / Magic Link token"""
    __tablename__ = 'otp_tokens'

    email = db.Column(db.String(255), nullable=False, index=True)
    code = db.Column(db.String(100), nullable=False)
    token_type = db.Column(db.String(20), nullable=False)  # 'otp' or 'magic_link'
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)

    @staticmethod
    def generate_otp(length=6):
        """Generate a numeric OTP code"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    def generate_magic_token():
        """Generate a secure magic link token"""
        return secrets.token_urlsafe(32)

    @property
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at.replace(tzinfo=timezone.utc)

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired and self.attempts < 5

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'token_type': self.token_type,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used,
        }
