from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = (kwargs.get("title") or "").strip()
        self.description = (kwargs.get("description") or "").strip()
        self.price = float(kwargs.get("price", 0))
        self.latitude = float(kwargs.get("latitude", 0))
        self.longitude = float(kwargs.get("longitude", 0))
        self.owner_id = (kwargs.get("owner_id") or "").strip()
        self.amenity_ids = list(kwargs.get("amenity_ids", []))

    def validate(self):
        """Validate place attributes."""
        # Title validation
        if not self.title:
            return False, "Title is required"
        if not isinstance(self.title, str):
            return False, "Title must be a string"
        if len(self.title) > 100:
            return False, "Title must be under 100 characters"
        
        # Price validation
        if not isinstance(self.price, (int, float)):
            return False, "Price must be a number"
        if self.price <= 0:
            return False, "Price must be greater than 0"
        if self.price > 1000000:
            return False, "Price must be under 1,000,000"
        
        # Latitude validation
        if not isinstance(self.latitude, (int, float)):
            return False, "Latitude must be a number"
        if not (-90 <= self.latitude <= 90):
            return False, "Latitude must be between -90 and 90"
        
        # Longitude validation
        if not isinstance(self.longitude, (int, float)):
            return False, "Longitude must be a number"
        if not (-180 <= self.longitude <= 180):
            return False, "Longitude must be between -180 and 180"
        
        # Owner validation
        if not self.owner_id:
            return False, "Owner ID is required"
        if not isinstance(self.owner_id, str):
            return False, "Owner ID must be a string"
        
        # Description is optional but has length limit
        if self.description and len(self.description) > 1000:
            return False, "Description must be under 1000 characters"
        
        # Amenity IDs validation
        if not isinstance(self.amenity_ids, list):
            return False, "Amenity IDs must be a list"
        
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
