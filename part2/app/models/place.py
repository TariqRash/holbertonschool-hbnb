from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get("title", "").strip()
        self.description = kwargs.get("description", "").strip()
        self.price = float(kwargs.get("price", 0))
        self.latitude = float(kwargs.get("latitude", 0))
        self.longitude = float(kwargs.get("longitude", 0))
        self.owner_id = kwargs.get("owner_id", "").strip()
        self.amenity_ids = list(kwargs.get("amenity_ids", []))

    def validate(self):
        if not self.title:
            return False, "Title is required"
        if self.price <= 0:
            return False, "Price must be greater than 0"
        if not (-90 <= self.latitude <= 90):
            return False, "Latitude must be between -90 and 90"
        if not (-180 <= self.longitude <= 180):
            return False, "Longitude must be between -180 and 180"
        if not self.owner_id:
            return False, "Owner ID is required"
        return True, None

    def add_amenity(self, amenity_id: str):
        if amenity_id and amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)

    def remove_amenity(self, amenity_id: str):
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "owner_id": self.owner_id,
                "amenity_ids": self.amenity_ids,
            }
        )
        return data
