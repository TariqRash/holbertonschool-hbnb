"""Unit tests for Review model."""
import unittest
from app.models.review import Review


class TestReview(unittest.TestCase):
    """Test cases for Review model."""

    def test_review_initialization(self):
        """Test review initialization with valid data."""
        review = Review(
            text="Great place to stay!",
            rating=5,
            user_id="user-123",
            place_id="place-456"
        )
        self.assertEqual(review.text, "Great place to stay!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, "user-123")
        self.assertEqual(review.place_id, "place-456")

    def test_review_validation_valid(self):
        """Test validation with valid review data."""
        review = Review(
            text="Excellent location and service",
            rating=4,
            user_id="user-789",
            place_id="place-012"
        )
        is_valid, error = review.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_review_validation_no_text(self):
        """Test validation fails when text is missing."""
        review = Review(
            text="",
            rating=3,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Review text is required")

    def test_review_validation_text_too_short(self):
        """Test validation fails when text is too short."""
        review = Review(
            text="Short",
            rating=3,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Review text must be at least 10 characters")

    def test_review_validation_text_too_long(self):
        """Test validation fails when text is too long."""
        review = Review(
            text="T" * 1001,
            rating=3,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Review text must be under 1000 characters")

    def test_review_validation_rating_too_low(self):
        """Test validation fails with rating below 1."""
        review = Review(
            text="Not good at all",
            rating=0,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Rating must be between 1 and 5")

    def test_review_validation_rating_too_high(self):
        """Test validation fails with rating above 5."""
        review = Review(
            text="Beyond excellent",
            rating=6,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Rating must be between 1 and 5")

    def test_review_validation_no_user_id(self):
        """Test validation fails when user_id is missing."""
        review = Review(
            text="Good place to stay",
            rating=4,
            user_id="",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "User ID is required")

    def test_review_validation_no_place_id(self):
        """Test validation fails when place_id is missing."""
        review = Review(
            text="Good place to stay",
            rating=4,
            user_id="user-1",
            place_id=""
        )
        is_valid, error = review.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Place ID is required")

    def test_review_validation_all_ratings(self):
        """Test validation succeeds for all valid ratings (1-5)."""
        for rating in range(1, 6):
            review = Review(
                text="Valid review text here",
                rating=rating,
                user_id="user-1",
                place_id="place-1"
            )
            is_valid, error = review.validate()
            self.assertTrue(is_valid, f"Rating {rating} should be valid")
            self.assertIsNone(error)

    def test_review_to_dict(self):
        """Test to_dict method."""
        review = Review(
            text="Amazing experience!",
            rating=5,
            user_id="user-999",
            place_id="place-888"
        )
        review_dict = review.to_dict()
        self.assertIn("text", review_dict)
        self.assertIn("rating", review_dict)
        self.assertIn("user_id", review_dict)
        self.assertIn("place_id", review_dict)
        self.assertIn("id", review_dict)

    def test_review_strip_whitespace(self):
        """Test that whitespace is stripped from string fields."""
        review = Review(
            text="  Great place!  ",
            rating=5,
            user_id="  user-123  ",
            place_id="  place-456  "
        )
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.user_id, "user-123")
        self.assertEqual(review.place_id, "place-456")

    def test_review_rating_conversion_to_int(self):
        """Test that rating is converted to integer."""
        review = Review(
            text="Good service overall",
            rating=4.7,  # Float input
            user_id="user-1",
            place_id="place-1"
        )
        self.assertIsInstance(review.rating, int)
        self.assertEqual(review.rating, 4)

    def test_review_minimum_valid_text_length(self):
        """Test review with minimum valid text length."""
        review = Review(
            text="Ten chars!",  # Exactly 10 characters
            rating=3,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_review_maximum_valid_text_length(self):
        """Test review with maximum valid text length."""
        review = Review(
            text="T" * 1000,  # Exactly 1000 characters
            rating=3,
            user_id="user-1",
            place_id="place-1"
        )
        is_valid, error = review.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
