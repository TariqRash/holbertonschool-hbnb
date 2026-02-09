# Amenity SQLAlchemy model
from app import db
from .base_model import BaseModel
from .associations import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = db.Column(db.String(255), unique=True, nullable=False)

    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )
