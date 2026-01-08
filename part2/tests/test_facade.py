"""Integration tests for Facade pattern."""
import unittest
from app.services.facade import Facade
from app.persistence.repository import Repository


class TestFacade(unittest.TestCase):
    """Test cases for Facade integration."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.facade = Facade()
        # Clear repository before each test
        self.facade.repo._storage = {}

    def tearDown(self):
        """Clean up after each test."""
        self.facade.repo._storage = {}

    # User tests
    def test_create_and_get_user(self):
        """Test creating and retrieving a user."""
        user = self.facade.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")
        
        retrieved_user = self.facade.get_user(user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_list_users(self):
        """Test listing all users."""
        user1 = self.facade.create_user(
            email="user1@example.com",
            password="pass123"
        )
        user2 = self.facade.create_user(
            email="user2@example.com",
            password="pass456"
        )
        
        users = self.facade.list_users()
        self.assertEqual(len(users), 2)
        emails = [u.email for u in users]
        self.assertIn("user1@example.com", emails)
        self.assertIn("user2@example.com", emails)

    def test_update_user(self):
        """Test updating a user."""
        user = self.facade.create_user(
            email="original@example.com",
            password="password123"
        )
        
        updated_user = self.facade.update_user(
            user.id,
            first_name="Updated",
            last_name="Name"
        )
        
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Name")
        self.assertEqual(updated_user.email, "original@example.com")

    def test_update_nonexistent_user(self):
        """Test updating a user that doesn't exist."""
        result = self.facade.update_user(
            "nonexistent-id",
            first_name="Test"
        )
        self.assertIsNone(result)

    # Amenity tests
    def test_create_and_get_amenity(self):
        """Test creating and retrieving an amenity."""
        amenity = self.facade.create_amenity(
            name="WiFi",
            description="High-speed internet"
        )
        self.assertIsNotNone(amenity)
        self.assertEqual(amenity.name, "WiFi")
        
        retrieved = self.facade.get_amenity(amenity.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, amenity.id)

    def test_list_amenities(self):
        """Test listing all amenities."""
        self.facade.create_amenity(name="Pool")
        self.facade.create_amenity(name="Gym")
        self.facade.create_amenity(name="Parking")
        
        amenities = self.facade.list_amenities()
        self.assertEqual(len(amenities), 3)

    def test_update_amenity(self):
        """Test updating an amenity."""
        amenity = self.facade.create_amenity(name="Old Name")
        
        updated = self.facade.update_amenity(
            amenity.id,
            name="New Name",
            description="Updated description"
        )
        
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "New Name")
        self.assertEqual(updated.description, "Updated description")

    # Place tests
    def test_create_place_with_valid_owner(self):
        """Test creating a place with a valid owner."""
        user = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        
        place = self.facade.create_place(
            title="Beach House",
            description="Beautiful view",
            price=200.0,
            latitude=40.0,
            longitude=-70.0,
            owner_id=user.id
        )
        
        self.assertIsNotNone(place)
        self.assertEqual(place.owner_id, user.id)

    def test_create_place_with_invalid_owner(self):
        """Test creating a place with invalid owner fails."""
        place = self.facade.create_place(
            title="House",
            description="Nice house",
            price=150.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="nonexistent-owner"
        )
        
        self.assertIsNone(place)

    def test_create_place_with_amenities(self):
        """Test creating a place with valid amenities."""
        user = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        amenity1 = self.facade.create_amenity(name="WiFi")
        amenity2 = self.facade.create_amenity(name="Pool")
        
        place = self.facade.create_place(
            title="Villa",
            description="Luxury villa",
            price=500.0,
            latitude=30.0,
            longitude=-80.0,
            owner_id=user.id,
            amenity_ids=[amenity1.id, amenity2.id]
        )
        
        self.assertIsNotNone(place)
        self.assertEqual(len(place.amenity_ids), 2)
        self.assertIn(amenity1.id, place.amenity_ids)
        self.assertIn(amenity2.id, place.amenity_ids)

    def test_create_place_with_invalid_amenity(self):
        """Test creating a place with invalid amenity fails."""
        user = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        
        place = self.facade.create_place(
            title="House",
            description="House",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=user.id,
            amenity_ids=["nonexistent-amenity"]
        )
        
        self.assertIsNone(place)

    def test_list_places(self):
        """Test listing all places."""
        user = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        
        self.facade.create_place(
            title="Place 1",
            description="Desc 1",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=user.id
        )
        self.facade.create_place(
            title="Place 2",
            description="Desc 2",
            price=200.0,
            latitude=10.0,
            longitude=20.0,
            owner_id=user.id
        )
        
        places = self.facade.list_places()
        self.assertEqual(len(places), 2)

    def test_update_place(self):
        """Test updating a place."""
        user = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        place = self.facade.create_place(
            title="Original Title",
            description="Original",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=user.id
        )
        
        updated = self.facade.update_place(
            place.id,
            title="Updated Title",
            price=150.0
        )
        
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.price, 150.0)

    # Review tests
    def test_create_review_with_valid_user_and_place(self):
        """Test creating a review with valid user and place."""
        user = self.facade.create_user(
            email="reviewer@example.com",
            password="password123"
        )
        owner = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        place = self.facade.create_place(
            title="House",
            description="Nice",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )
        
        review = self.facade.create_review(
            user_id=user.id,
            place_id=place.id,
            rating=5,
            text="Excellent place!"
        )
        
        self.assertIsNotNone(review)
        self.assertEqual(review.user_id, user.id)
        self.assertEqual(review.place_id, place.id)
        self.assertEqual(review.rating, 5)

    def test_create_review_with_invalid_user(self):
        """Test creating a review with invalid user fails."""
        owner = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        place = self.facade.create_place(
            title="House",
            description="Nice",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )
        
        review = self.facade.create_review(
            user_id="nonexistent-user",
            place_id=place.id,
            rating=5,
            text="Great!"
        )
        
        self.assertIsNone(review)

    def test_create_review_with_invalid_place(self):
        """Test creating a review with invalid place fails."""
        user = self.facade.create_user(
            email="user@example.com",
            password="password123"
        )
        
        review = self.facade.create_review(
            user_id=user.id,
            place_id="nonexistent-place",
            rating=5,
            text="Great!"
        )
        
        self.assertIsNone(review)

    def test_list_reviews_for_place(self):
        """Test listing reviews for a specific place."""
        user = self.facade.create_user(
            email="user@example.com",
            password="password123"
        )
        owner = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        place = self.facade.create_place(
            title="House",
            description="Nice",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )
        
        self.facade.create_review(
            user_id=user.id,
            place_id=place.id,
            rating=5,
            text="Excellent place!"
        )
        self.facade.create_review(
            user_id=user.id,
            place_id=place.id,
            rating=4,
            text="Good place!"
        )
        
        reviews = self.facade.list_reviews_for_place(place.id)
        self.assertIsNotNone(reviews)
        self.assertEqual(len(reviews), 2)

    def test_delete_review(self):
        """Test deleting a review."""
        user = self.facade.create_user(
            email="user@example.com",
            password="password123"
        )
        owner = self.facade.create_user(
            email="owner@example.com",
            password="password123"
        )
        place = self.facade.create_place(
            title="House",
            description="Nice",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )
        review = self.facade.create_review(
            user_id=user.id,
            place_id=place.id,
            rating=5,
            text="Great place!"
        )
        
        # Delete the review
        result = self.facade.delete_review(review.id)
        self.assertTrue(result)
        
        # Verify it's deleted
        deleted_review = self.facade.get_review(review.id)
        self.assertIsNone(deleted_review)

    def test_delete_nonexistent_review(self):
        """Test deleting a review that doesn't exist."""
        result = self.facade.delete_review("nonexistent-id")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
