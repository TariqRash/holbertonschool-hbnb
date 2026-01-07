"""Place Model - Manages property listings"""
from app.models.base_entity import BaseEntity


class Place(BaseEntity):
    """Place entity for property listings"""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize a new Place instance"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner.id
        self.amenities = []
        self.reviews = []
        self._validate()

    def _validate(self):
        """Validate place attributes"""
        # Validate title
        if not self.title or len(self.title) < 5 or len(self.title) > 100:
            raise ValueError("Title must be between 5 and 100 characters")
        
        # Validate description
        if not self.description or len(self.description) > 1000:
            raise ValueError("Description is required and cannot exceed 1000 characters")
        
        # Validate price
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive number")
        
        # Validate coordinates
        if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def calculate_average_rating(self):
        """Calculate average rating from all reviews"""
        if not self.reviews:
            return 0.0
        total = sum(review.rating for review in self.reviews)
        return total / len(self.reviews)

    def to_dict(self):
        """Convert place to dictionary representation"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        return data
