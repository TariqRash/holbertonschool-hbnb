"""Review Model - Manages place reviews and ratings"""
from app.models.base_entity import BaseEntity


class Review(BaseEntity):
    """Review entity for place ratings and feedback"""

    def __init__(self, place, user, rating, comment):
        """Initialize a new Review instance"""
        super().__init__()
        self.place = place
        self.place_id = place.id
        self.user = user
        self.user_id = user.id
        self.rating = rating
        self.comment = comment
        self._validate()

    def _validate(self):
        """Validate review attributes"""
        # Validate rating
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate comment
        if not self.comment or len(self.comment) > 500:
            raise ValueError("Comment is required and cannot exceed 500 characters")
        
        # Validate user cannot review own place
        if self.user_id == self.place.owner_id:
            raise ValueError("Users cannot review their own places")

    def to_dict(self):
        """Convert review to dictionary representation"""
        data = super().to_dict()
        data.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment
        })
        return data
