"""
HBnB V2 — Media Model
Property images and gallery management.
"""
from app import db
from app.models.base_model import BaseModel


class Media(BaseModel):
    """Media model — property images"""
    __tablename__ = 'media'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    caption_en = db.Column(db.String(200), nullable=True)
    caption_ar = db.Column(db.String(200), nullable=True)
    media_type = db.Column(db.String(20), default='image')  # image, video
    sort_order = db.Column(db.Integer, default=0)
    is_cover = db.Column(db.Boolean, default=False)

    def to_dict(self, lang='ar'):
        return {
            'id': self.id,
            'url': self.url,
            'thumbnail_url': self.thumbnail_url,
            'caption': self.caption_ar if lang == 'ar' else self.caption_en,
            'media_type': self.media_type,
            'is_cover': self.is_cover,
            'sort_order': self.sort_order,
        }
