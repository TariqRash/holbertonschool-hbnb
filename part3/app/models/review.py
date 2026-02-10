# Review SQLAlchemy model
from app import db
from .base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))

    user = db.relationship(
        "User",
        back_populates="reviews"
    )
    place = db.relationship(
        "Place",
        back_populates="reviews"
    )
