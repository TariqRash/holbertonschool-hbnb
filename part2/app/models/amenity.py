from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = (kwargs.get("name") or "").strip()
        self.description = (kwargs.get("description") or "").strip()

    def validate(self):
        """Validate amenity attributes."""
        if not self.name:
            return False, "Amenity name is required"
        if not isinstance(self.name, str):
            return False, "Amenity name must be a string"
        if len(self.name) > 100:
            return False, "Amenity name must be under 100 characters"
        if len(self.name) < 1:
            return False, "Amenity name cannot be empty"
        
        # Description is optional but has length limit
        if self.description and len(self.description) > 500:
            return False, "Description must be under 500 characters"
        
        return True, None

    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name, "description": self.description})
        return data
