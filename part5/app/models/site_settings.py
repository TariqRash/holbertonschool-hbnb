"""
HBnB V2 — Site Settings Model
Admin-manageable API keys, app configuration, and feature flags.
"""
from app import db
from app.models.base_model import BaseModel


class SiteSetting(BaseModel):
    """Key-value store for admin-configurable settings"""
    __tablename__ = 'site_settings'

    key = db.Column(db.String(100), nullable=False, unique=True, index=True)
    value = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='general')  # general, api_keys, booking, appearance
    description_en = db.Column(db.String(255), nullable=True)
    description_ar = db.Column(db.String(255), nullable=True)
    is_secret = db.Column(db.Boolean, default=False)  # Mask value in responses

    def to_dict(self, include_secrets=False):
        val = self.value
        if self.is_secret and not include_secrets and val:
            val = val[:4] + '****' + val[-4:] if len(val) > 8 else '****'
        return {
            'id': self.id,
            'key': self.key,
            'value': val,
            'category': self.category,
            'description_en': self.description_en,
            'description_ar': self.description_ar,
            'is_secret': self.is_secret,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def get_value(key, default=None):
        """Get a setting value by key"""
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_value(key, value, category='general', description_en=None, description_ar=None, is_secret=False):
        """Set a setting value, create if not exists"""
        setting = SiteSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SiteSetting(
                key=key,
                value=value,
                category=category,
                description_en=description_en,
                description_ar=description_ar,
                is_secret=is_secret,
            )
            db.session.add(setting)
        db.session.commit()
        return setting
