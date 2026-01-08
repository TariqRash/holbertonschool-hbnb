from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = (kwargs.get("text") or "").strip()
        self.rating = int(kwargs.get("rating", 0))
        self.user_id = (kwargs.get("user_id") or "").strip()
        self.place_id = (kwargs.get("place_id") or "").strip()

    def validate(self):
        """Validate review attributes."""
        # Text validation
        if not self.text:
            return False, "Review text is required"
        if not isinstance(self.text, str):
            return False, "Review text must be a string"
        if len(self.text) < 10:
            return False, "Review text must be at least 10 characters"
        if len(self.text) > 1000:
            return False, "Review text must be under 1000 characters"
        
        # Rating validation
        if not isinstance(self.rating, int):
            return False, "Rating must be an integer"
        if not 1 <= self.rating <= 5:
            return False, "Rating must be between 1 and 5"
        
        # User ID validation
        if not self.user_id:
            return False, "User ID is required"
        if not isinstance(self.user_id, str):
            return False, "User ID must be a string"
        
        # Place ID validation
        if not self.place_id:
            return False, "Place ID is required"
        if not isinstance(self.place_id, str):
            return False, "Place ID must be a string"
        
        return True, None

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "text": self.text,
                "rating": self.rating,
                "user_id": self.user_id,
                "place_id": self.place_id,
            }
        )
        return data
