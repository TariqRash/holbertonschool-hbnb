"""Facade Pattern Implementation - Simplifies communication between layers"""
from app.models import User, Place, Review, Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Facade for managing business logic operations"""

    def __init__(self):
        """Initialize facade with repositories for each entity type"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        # Check if email already exists
        if self.user_repo.get_by_attribute('email', user.email):
            raise ValueError("User with this email already exists")
        
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user"""
        return self.user_repo.update(user_id, user_data)

    # Place operations
    def create_place(self, place_data):
        """Create a new place"""
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        
        # Add amenities if provided
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
        
        owner.add_place(place)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place"""
        return self.place_repo.delete(place_id)

    # Review operations
    def create_review(self, review_data):
        """Create a new review"""
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
        
        review = Review(
            place=place,
            user=user,
            rating=review_data['rating'],
            comment=review_data['comment']
        )
        
        place.add_review(review)
        user.add_review(review)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = self.get_place(place_id)
        return place.reviews if place else []

    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    # Amenity operations
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(
            name=amenity_data['name'],
            description=amenity_data.get('description', '')
        )
        
        # Check if amenity name already exists
        if self.amenity_repo.get_by_attribute('name', amenity.name):
            raise ValueError("Amenity with this name already exists")
        
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        return self.amenity_repo.delete(amenity_id)
