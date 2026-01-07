"""User Model - Handles user management and authentication"""
import re
from app.models.base_entity import BaseEntity


class User(BaseEntity):
    """User entity for managing user accounts"""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a new User instance"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.owned_places = []
        self.reviews = []
        self._validate()

    def _validate(self):
        """Validate user attributes"""
        # Validate first_name
        if not self.first_name or len(self.first_name) < 2 or len(self.first_name) > 50:
            raise ValueError("First name must be between 2 and 50 characters")
        
        # Validate last_name
        if not self.last_name or len(self.last_name) < 2 or len(self.last_name) > 50:
            raise ValueError("Last name must be between 2 and 50 characters")
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not self.email or not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

    def add_place(self, place):
        """Add a place to user's owned places"""
        if place not in self.owned_places:
            self.owned_places.append(place)

    def add_review(self, review):
        """Add a review written by the user"""
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """Convert user to dictionary representation"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data
