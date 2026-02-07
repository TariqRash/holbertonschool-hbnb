"""Unit tests for Amenity model."""
import unittest
from app.models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity model."""

    def test_amenity_initialization(self):
        """Test amenity initialization with valid data."""
        amenity = Amenity(name="WiFi", description="High-speed internet")
        self.assertEqual(amenity.name, "WiFi")
        self.assertEqual(amenity.description, "High-speed internet")

    def test_amenity_default_values(self):
        """Test amenity initialization with default values."""
        amenity = Amenity(name="Pool")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.description, "")

    def test_amenity_validation_valid(self):
        """Test validation with valid amenity data."""
        amenity = Amenity(name="Parking", description="Free parking space")
        is_valid, error = amenity.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_amenity_validation_no_name(self):
        """Test validation fails when name is missing."""
        amenity = Amenity(name="", description="Some description")
        is_valid, error = amenity.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Amenity name is required")

    def test_amenity_validation_name_too_long(self):
        """Test validation fails when name is too long."""
        amenity = Amenity(name="A" * 51, description="Description")
        is_valid, error = amenity.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Amenity name must be under 50 characters")

    def test_amenity_validation_description_too_long(self):
        """Test validation fails when description is too long."""
        amenity = Amenity(name="Gym", description="D" * 501)
        is_valid, error = amenity.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Description must be under 500 characters")

    def test_amenity_validation_valid_with_no_description(self):
        """Test validation succeeds with no description."""
        amenity = Amenity(name="Air Conditioning")
        is_valid, error = amenity.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_amenity_to_dict(self):
        """Test to_dict method."""
        amenity = Amenity(name="Kitchen", description="Fully equipped")
        amenity_dict = amenity.to_dict()
        self.assertIn("name", amenity_dict)
        self.assertIn("description", amenity_dict)
        self.assertIn("id", amenity_dict)
        self.assertEqual(amenity_dict["name"], "Kitchen")
        self.assertEqual(amenity_dict["description"], "Fully equipped")

    def test_amenity_strip_whitespace(self):
        """Test that whitespace is stripped from string fields."""
        amenity = Amenity(
            name="  Swimming Pool  ",
            description="  Olympic size  "
        )
        self.assertEqual(amenity.name, "Swimming Pool")
        self.assertEqual(amenity.description, "Olympic size")

    def test_amenity_validation_only_whitespace_name(self):
        """Test validation fails when name is only whitespace."""
        amenity = Amenity(name="   ", description="Description")
        is_valid, error = amenity.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Amenity name is required")

    def test_amenity_max_length_name(self):
        """Test amenity with maximum allowed name length."""
        amenity = Amenity(name="A" * 50, description="Valid")
        is_valid, error = amenity.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_amenity_max_length_description(self):
        """Test amenity with maximum allowed description length."""
        amenity = Amenity(name="Gym", description="D" * 500)
        is_valid, error = amenity.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
