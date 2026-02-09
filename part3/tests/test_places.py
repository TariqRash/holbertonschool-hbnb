"""Tests for Place API endpoints"""
import unittest
from app import create_app, db
from app.models.place import Place
from app.models.user import User


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place API"""
    
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
    
    def test_get_places_returns_200(self):
        """Test GET /api/v1/places/ returns 200"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_nonexistent_place_returns_404(self):
        """Test GET /api/v1/places/<id> returns 404 for invalid ID"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_create_place_requires_auth(self):
        """Test POST /api/v1/places/ requires authentication"""
        response = self.client.post('/api/v1/places/',
            json={
                "title": "Test Place",
                "description": "A test place",
                "price": 100.00,
                "latitude": 25.0,
                "longitude": 45.0
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_update_place_requires_auth(self):
        """Test PUT /api/v1/places/<id> requires authentication"""
        response = self.client.put('/api/v1/places/some-id',
            json={"title": "Updated Title"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_delete_place_requires_auth(self):
        """Test DELETE /api/v1/places/<id> requires authentication"""
        response = self.client.delete('/api/v1/places/some-id')
        self.assertEqual(response.status_code, 401)


class TestPlaceModel(unittest.TestCase):
    """Test cases for Place model"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.app = create_app("config.TestingConfig")
    
    def test_place_creation(self):
        """Test Place model can be instantiated"""
        with self.app.app_context():
            place = Place(
                title="Beach House",
                description="Beautiful beach house",
                price=150.00,
                latitude=25.5,
                longitude=45.5,
                owner_id="test-owner-id"
            )
            self.assertEqual(place.title, "Beach House")
            self.assertEqual(place.price, 150.00)
            db.session.add(place)
            db.session.flush()
            self.assertIsNotNone(place.id)
            db.session.rollback()


if __name__ == '__main__':
    unittest.main()
