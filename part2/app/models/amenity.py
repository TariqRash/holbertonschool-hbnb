"""Amenity Model - Manages reusable place features"""
from app.models.base_entity import BaseEntity


class Amenity(BaseEntity):
    """Amenity entity for place features"""

    def __init__(self, name, description=""):
        """Initialize a new Amenity instance"""
        super().__init__()
        self.name = name
        self.description = description
        self._validate()

    def _validate(self):
        """Validate amenity attributes"""
        # Validate name
        if not self.name or len(self.name) < 3 or len(self.name) > 50:
            raise ValueError("Amenity name must be between 3 and 50 characters")
        
        # Validate description
        if self.description and len(self.description) > 200:
            raise ValueError("Description cannot exceed 200 characters")

    def to_dict(self):
        """Convert amenity to dictionary representation"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description
        })
        return data
