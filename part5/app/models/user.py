"""
HBnB V2 — User Model
Supports: guest, owner, admin roles
Auth: OTP, Magic Link, password (fallback)
"""
from app import db
from app.models.base_model import BaseModel
import bcrypt

# Many-to-many: User <-> Favorite Places
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True)
)


class User(BaseModel):
    """User model — guests, owners, and admins"""
    __tablename__ = 'users'

    # Profile
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True) # Mobile
    sex = db.Column(db.String(10), nullable=True)   # male, female

    # Auth
    password_hash = db.Column(db.String(255), nullable=True)  # Optional (magic link users may not have one)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Role: guest, owner, admin
    role = db.Column(db.String(20), default='guest', nullable=False)

    # Favorites
    favorites = db.relationship('Place', secondary=user_favorites, backref='favorited_by', lazy='dynamic')

    # Localization
    preferred_language = db.Column(db.String(5), default='ar')
    country = db.Column(db.String(5), default='SA')

    # Relationships
    places = db.relationship('Place', backref='owner', lazy='dynamic', foreign_keys='Place.owner_id')
    bookings = db.relationship('Booking', backref='guest', lazy='dynamic', foreign_keys='Booking.guest_id')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        """Verify password"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_owner(self):
        return self.role in ('owner', 'admin')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self, include_private=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email if include_private else None,
            'phone': self.phone if include_private else None,
            'sex': self.sex if include_private else None,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'role': self.role,
            'is_verified': self.is_verified,
            'preferred_language': self.preferred_language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if not include_private:
            data.pop('email', None)
            data.pop('phone', None)
            data.pop('sex', None)
        return data

    def to_public_dict(self):
        """Public profile — no sensitive info"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
