# Place SQLAlchemy model

from app import db
from .base_model import BaseModel
from .associations import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'))

    owner = db.relationship(
        "User",
        back_populates="places"
    )
    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan"
    )
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places"
    )
