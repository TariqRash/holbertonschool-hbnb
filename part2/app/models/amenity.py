from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "").strip()
        self.description = kwargs.get("description", "").strip()

    def validate(self):
        if not self.name:
            return False, "Amenity name is required"
        if len(self.name) > 100:
            return False, "Amenity name must be under 100 characters"
        return True, None

    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name, "description": self.description})
        return data
