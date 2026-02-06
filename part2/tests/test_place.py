"""Unit tests for Place model."""
import unittest
from app.models.place import Place


class TestPlace(unittest.TestCase):
    """Test cases for Place model."""

    def test_place_initialization(self):
        """Test place initialization with valid data."""
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id="user-123",
            amenity_ids=["amenity-1", "amenity-2"]
        )
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.description, "A nice place to stay")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner_id, "user-123")
        self.assertEqual(place.amenity_ids, ["amenity-1", "amenity-2"])

    def test_place_default_values(self):
        """Test place initialization with default values."""
        place = Place(
            title="House",
            price=150.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        self.assertEqual(place.description, "")
        self.assertEqual(place.amenity_ids, [])

    def test_place_validation_valid(self):
        """Test validation with valid place data."""
        place = Place(
            title="Beach House",
            price=200.0,
            latitude=25.7617,
            longitude=-80.1918,
            owner_id="owner-456"
        )
        is_valid, error = place.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_place_validation_no_title(self):
        """Test validation fails when title is missing."""
        place = Place(
            title="",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Title is required")

    def test_place_validation_title_too_long(self):
        """Test validation fails when title is too long."""
        place = Place(
            title="T" * 101,
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Title must be under 100 characters")

    def test_place_validation_negative_price(self):
        """Test validation fails with negative price."""
        place = Place(
            title="House",
            price=-50.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Price must be greater than 0")

    def test_place_validation_zero_price(self):
        """Test validation fails with zero price."""
        place = Place(
            title="House",
            price=0.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Price must be greater than 0")

    def test_place_validation_price_too_high(self):
        """Test validation fails with price exceeding maximum."""
        place = Place(
            title="Luxury Villa",
            price=1000001.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Price must be under 1,000,000")

    def test_place_validation_latitude_too_low(self):
        """Test validation fails with latitude below -90."""
        place = Place(
            title="House",
            price=100.0,
            latitude=-91.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Latitude must be between -90 and 90")

    def test_place_validation_latitude_too_high(self):
        """Test validation fails with latitude above 90."""
        place = Place(
            title="House",
            price=100.0,
            latitude=91.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Latitude must be between -90 and 90")

    def test_place_validation_longitude_too_low(self):
        """Test validation fails with longitude below -180."""
        place = Place(
            title="House",
            price=100.0,
            latitude=0.0,
            longitude=-181.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Longitude must be between -180 and 180")

    def test_place_validation_longitude_too_high(self):
        """Test validation fails with longitude above 180."""
        place = Place(
            title="House",
            price=100.0,
            latitude=0.0,
            longitude=181.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Longitude must be between -180 and 180")

    def test_place_validation_no_owner_id(self):
        """Test validation fails when owner_id is missing."""
        place = Place(
            title="House",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=""
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Owner ID is required")

    def test_place_validation_description_too_long(self):
        """Test validation fails when description is too long."""
        place = Place(
            title="House",
            description="D" * 1001,
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        is_valid, error = place.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Description must be under 1000 characters")

    def test_place_add_amenity(self):
        """Test adding amenities to a place."""
        place = Place(
            title="House",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1"
        )
        place.add_amenity("amenity-1")
        self.assertIn("amenity-1", place.amenity_ids)
        
        # Adding duplicate should not add twice
        place.add_amenity("amenity-1")
        self.assertEqual(place.amenity_ids.count("amenity-1"), 1)

    def test_place_remove_amenity(self):
        """Test removing amenities from a place."""
        place = Place(
            title="House",
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-1",
            amenity_ids=["amenity-1", "amenity-2"]
        )
        place.remove_amenity("amenity-1")
        self.assertNotIn("amenity-1", place.amenity_ids)
        self.assertIn("amenity-2", place.amenity_ids)

    def test_place_to_dict(self):
        """Test to_dict method."""
        place = Place(
            title="Villa",
            description="Luxury villa",
            price=500.0,
            latitude=40.0,
            longitude=-70.0,
            owner_id="owner-789",
            amenity_ids=["amenity-1"]
        )
        place_dict = place.to_dict()
        self.assertIn("title", place_dict)
        self.assertIn("description", place_dict)
        self.assertIn("price", place_dict)
        self.assertIn("latitude", place_dict)
        self.assertIn("longitude", place_dict)
        self.assertIn("owner_id", place_dict)
        self.assertIn("amenity_ids", place_dict)

    def test_place_strip_whitespace(self):
        """Test that whitespace is stripped from string fields."""
        place = Place(
            title="  Beach House  ",
            description="  Beautiful view  ",
            price=200.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="  owner-1  "
        )
        self.assertEqual(place.title, "Beach House")
        self.assertEqual(place.description, "Beautiful view")
        self.assertEqual(place.owner_id, "owner-1")


if __name__ == "__main__":
    unittest.main()
