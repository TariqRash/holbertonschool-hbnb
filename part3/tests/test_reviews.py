"""Tests for Review API endpoints"""
import unittest
from app import create_app, db
from app.models.review import Review


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review API"""
    
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
    
    def test_get_reviews_returns_200(self):
        """Test GET /api/v1/reviews/ returns 200"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_nonexistent_review_returns_404(self):
        """Test GET /api/v1/reviews/<id> returns 404 for invalid ID"""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_create_review_requires_auth(self):
        """Test POST /api/v1/reviews/ requires authentication"""
        response = self.client.post('/api/v1/reviews/',
            json={
                "place_id": "test-place-id",
                "text": "Great place!",
                "rating": 5
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_update_review_requires_auth(self):
        """Test PUT /api/v1/reviews/<id> requires authentication"""
        response = self.client.put('/api/v1/reviews/some-id',
            json={"text": "Updated review", "rating": 4},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_delete_review_requires_auth(self):
        """Test DELETE /api/v1/reviews/<id> requires authentication"""
        response = self.client.delete('/api/v1/reviews/some-id')
        self.assertEqual(response.status_code, 401)


class TestReviewModel(unittest.TestCase):
    """Test cases for Review model"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.app = create_app("config.TestingConfig")
    
    def test_review_creation(self):
        """Test Review model can be instantiated"""
        with self.app.app_context():
            review = Review(
                text="Amazing experience!",
                rating=5,
                user_id="test-user-id",
                place_id="test-place-id"
            )
            self.assertEqual(review.text, "Amazing experience!")
            self.assertEqual(review.rating, 5)
            db.session.add(review)
            db.session.flush()
            self.assertIsNotNone(review.id)
            db.session.rollback()
    
    def test_review_rating_range(self):
        """Test review rating should be between 1-5"""
        with self.app.app_context():
            # Valid ratings
            for rating in [1, 2, 3, 4, 5]:
                review = Review(
                    text="Test",
                    rating=rating,
                    user_id="user-id",
                    place_id="place-id"
                )
                self.assertEqual(review.rating, rating)


if __name__ == '__main__':
    unittest.main()
