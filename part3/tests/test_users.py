"""Tests for User API endpoints"""
import unittest
from app import create_app, db
from app.models.user import User


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.app = create_app("config.TestingConfig")
        cls.client = cls.app.test_client()
        
        with cls.app.app_context():
            db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        with cls.app.app_context():
            db.drop_all()
    
    def test_get_users_returns_200(self):
        """Test GET /api/v1/users/ returns 200"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_nonexistent_user_returns_404(self):
        """Test GET /api/v1/users/<id> returns 404 for invalid ID"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user_requires_auth(self):
        """Test POST /api/v1/users/ requires authentication"""
        response = self.client.post('/api/v1/users/', 
            json={
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_update_user_requires_auth(self):
        """Test PUT /api/v1/users/<id> requires authentication"""
        response = self.client.put('/api/v1/users/some-id',
            json={"first_name": "Updated"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)


class TestUserModel(unittest.TestCase):
    """Test cases for User model"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.app = create_app("config.TestingConfig")
    
    def test_password_hashing(self):
        """Test password is properly hashed"""
        with self.app.app_context():
            user = User(
                first_name="Test",
                last_name="User",
                email="hash@test.com"
            )
            user.hash_password("mypassword123")
            
            # Password should be hashed, not plain text
            self.assertNotEqual(user.password, "mypassword123")
            self.assertTrue(user.password.startswith("$2b$"))
    
    def test_password_verification(self):
        """Test password verification works correctly"""
        with self.app.app_context():
            user = User(
                first_name="Test",
                last_name="User",
                email="verify@test.com"
            )
            user.hash_password("correctpassword")
            
            # Correct password should verify
            self.assertTrue(user.verify_password("correctpassword"))
            
            # Wrong password should not verify
            self.assertFalse(user.verify_password("wrongpassword"))


if __name__ == '__main__':
    unittest.main()
