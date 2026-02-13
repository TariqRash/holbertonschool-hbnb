"""
HBnB V2 — Amenity Model
With bilingual names and icons.
"""
from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity with icon support"""
    __tablename__ = 'amenities'

    name_en = db.Column(db.String(100), nullable=False, unique=True)
    name_ar = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=True)  # Lucide icon name (e.g., 'wifi', 'car', 'waves')
    category = db.Column(db.String(50), default='general')  # general, safety, kitchen, outdoor, etc.
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self, lang='ar'):
        return {
            'id': self.id,
            'name': self.name_ar if lang == 'ar' else self.name_en,
            'name_en': self.name_en,
            'name_ar': self.name_ar,
            'icon': self.icon,
            'category': self.category,
        }
