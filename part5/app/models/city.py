"""
HBnB V2 — City Model
Saudi cities with Arabic/English names and coordinates.
"""
from app import db
from app.models.base_model import BaseModel


class City(BaseModel):
    """City model — Saudi Arabia cities"""
    __tablename__ = 'cities'

    name_en = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    region_en = db.Column(db.String(100), nullable=True)
    region_ar = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    # Relationships
    places = db.relationship('Place', backref='city', lazy='dynamic')

    def to_dict(self, lang='ar'):
        return {
            'id': self.id,
            'name': self.name_ar if lang == 'ar' else self.name_en,
            'name_en': self.name_en,
            'name_ar': self.name_ar,
            'region': self.region_ar if lang == 'ar' else self.region_en,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'is_featured': self.is_featured,
            'place_count': self.places.count() if self.places else 0,
        }
