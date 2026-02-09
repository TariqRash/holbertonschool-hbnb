# Facade for business logic

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    """Facade pattern to simplify interaction with repositories"""
    
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_data):
        """Create a new user with hashed password"""
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            is_admin=user_data.get("is_admin", False)
        )
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update user (regular user - cannot change email/password)"""
        self.user_repo.update(user_id, data)

    def admin_update_user(self, user_id, data):
        """Admin update user (can change email/password)"""
        user = self.get_user(user_id)
        if not user:
            return None
        if "password" in data:
            user.hash_password(data["password"])
            self.user_repo.update(user_id, {"password": user.password})
            data = {k: v for k, v in data.items() if k != "password"}
        if data:
            self.user_repo.update(user_id, data)
        return user

    # ==================== PLACE OPERATIONS ====================
    
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        """Update place"""
        self.place_repo.update(place_id, data)

    def delete_place(self, place_id):
        """Delete place"""
        self.place_repo.delete(place_id)

    # ==================== REVIEW OPERATIONS ====================
    
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place_id == place_id]

    def get_review_by_user_and_place(self, user_id, place_id):
        """Check if user already reviewed a place"""
        return self.review_repo.get_by_attributes(user_id=user_id, place_id=place_id)

    def update_review(self, review_id, data):
        """Update review"""
        self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        """Delete review"""
        self.review_repo.delete(review_id)

    # ==================== AMENITY OPERATIONS ====================
    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        return self.amenity_repo.get_by_attribute("name", name)

    def update_amenity(self, amenity_id, data):
        """Update amenity"""
        self.amenity_repo.update(amenity_id, data)
