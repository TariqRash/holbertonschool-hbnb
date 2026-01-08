from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "").strip()
        self.rating = int(kwargs.get("rating", 0))
        self.user_id = kwargs.get("user_id", "").strip()
        self.place_id = kwargs.get("place_id", "").strip()

    def validate(self):
        if not self.text:
            return False, "Review text is required"
        if not 1 <= self.rating <= 5:
            return False, "Rating must be between 1 and 5"
        if not self.user_id:
            return False, "User ID is required"
        if not self.place_id:
            return False, "Place ID is required"
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
