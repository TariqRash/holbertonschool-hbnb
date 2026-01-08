"""Unit tests for User model."""
import unittest
from app.models.user import User


class TestUser(unittest.TestCase):
    """Test cases for User model."""

    def test_user_initialization(self):
        """Test user initialization with valid data."""
        user = User(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            is_admin=False
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertFalse(user.is_admin)

    def test_user_default_values(self):
        """Test user initialization with default values."""
        user = User(email="test@example.com", password="password123")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertFalse(user.is_admin)

    def test_user_validation_valid(self):
        """Test validation with valid user data."""
        user = User(email="valid@example.com", password="securepass")
        is_valid, error = user.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_user_validation_no_email(self):
        """Test validation fails when email is missing."""
        user = User(email="", password="password123")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Email is required")

    def test_user_validation_invalid_email_format(self):
        """Test validation fails with invalid email format."""
        user = User(email="invalid-email", password="password123")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_user_validation_no_at_symbol(self):
        """Test validation fails when email has no @ symbol."""
        user = User(email="invalidemail.com", password="password123")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_user_validation_short_password(self):
        """Test validation fails with short password."""
        user = User(email="test@example.com", password="12345")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Password must be at least 6 characters")

    def test_user_validation_no_password(self):
        """Test validation fails when password is missing."""
        user = User(email="test@example.com", password="")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Password is required")

    def test_user_validation_long_email(self):
        """Test validation fails with extremely long email."""
        long_email = "a" * 250 + "@test.com"
        user = User(email=long_email, password="password123")
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Email must be under 255 characters")

    def test_user_validation_long_first_name(self):
        """Test validation fails with long first name."""
        user = User(
            email="test@example.com",
            password="password123",
            first_name="A" * 51
        )
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "First name must be under 50 characters")

    def test_user_validation_long_last_name(self):
        """Test validation fails with long last name."""
        user = User(
            email="test@example.com",
            password="password123",
            last_name="B" * 51
        )
        is_valid, error = user.validate()
        self.assertFalse(is_valid)
        self.assertEqual(error, "Last name must be under 50 characters")

    def test_user_to_dict(self):
        """Test to_dict method excludes password."""
        user = User(
            email="test@example.com",
            password="secret123",
            first_name="Jane",
            last_name="Smith"
        )
        user_dict = user.to_dict()
        self.assertIn("email", user_dict)
        self.assertIn("first_name", user_dict)
        self.assertIn("last_name", user_dict)
        self.assertIn("is_admin", user_dict)
        self.assertNotIn("password", user_dict)

    def test_user_strip_whitespace(self):
        """Test that whitespace is stripped from string fields."""
        user = User(
            email="  test@example.com  ",
            password="password123",
            first_name="  John  ",
            last_name="  Doe  "
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_user_is_admin_bool_conversion(self):
        """Test is_admin is converted to boolean."""
        user1 = User(email="test@example.com", password="pass123", is_admin=1)
        user2 = User(email="test@example.com", password="pass123", is_admin=0)
        user3 = User(email="test@example.com", password="pass123", is_admin="true")
        
        self.assertTrue(user1.is_admin)
        self.assertFalse(user2.is_admin)
        self.assertTrue(user3.is_admin)


if __name__ == "__main__":
    unittest.main()
