"""
HBnB V2 — Review Model
"""
from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review model — with rating breakdown"""
    __tablename__ = 'reviews'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'), nullable=True)

    # Overall rating 1-5
    rating = db.Column(db.Integer, nullable=False)

    # Rating breakdown
    cleanliness = db.Column(db.Integer, nullable=True)
    accuracy = db.Column(db.Integer, nullable=True)
    location_rating = db.Column(db.Integer, nullable=True)
    value = db.Column(db.Integer, nullable=True)
    communication = db.Column(db.Integer, nullable=True)
    check_in_rating = db.Column(db.Integer, nullable=True)

    # Review text
    comment = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(5), default='ar')

    # Moderation
    is_approved = db.Column(db.Boolean, default=True)

    def to_dict(self, lang='ar'):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'rating': self.rating,
            'cleanliness': self.cleanliness,
            'accuracy': self.accuracy,
            'location_rating': self.location_rating,
            'value': self.value,
            'communication': self.communication,
            'check_in_rating': self.check_in_rating,
            'comment': self.comment,
            'language': self.language,
            'author': self.author.to_public_dict() if self.author else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
