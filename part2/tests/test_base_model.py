"""Unit tests for BaseModel class."""
import unittest
from datetime import datetime
from app.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel."""

    def test_initialization_default(self):
        """Test default initialization."""
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_initialization_with_kwargs(self):
        """Test initialization with keyword arguments."""
        custom_id = "test-id-123"
        custom_date = datetime(2024, 1, 1, 12, 0, 0)
        model = BaseModel(id=custom_id, created_at=custom_date, updated_at=custom_date)
        self.assertEqual(model.id, custom_id)
        self.assertEqual(model.created_at, custom_date)
        self.assertEqual(model.updated_at, custom_date)

    def test_to_dict(self):
        """Test to_dict method."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_touch(self):
        """Test touch method updates updated_at."""
        model = BaseModel()
        original_updated_at = model.updated_at
        import time
        time.sleep(0.01)  # Small delay to ensure timestamp difference
        model.touch()
        self.assertGreater(model.updated_at, original_updated_at)

    def test_update(self):
        """Test update method."""
        model = BaseModel()
        original_id = model.id
        original_created_at = model.created_at
        
        # Update shouldn't change id or created_at
        model.update(id="new-id", created_at=datetime.now())
        self.assertEqual(model.id, original_id)
        self.assertEqual(model.created_at, original_created_at)

    def test_unique_ids(self):
        """Test that each instance gets a unique ID."""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)


if __name__ == "__main__":
    unittest.main()
