"""API endpoint tests for all entities."""
import unittest
import json
from app import create_app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
        # Clear repository
        from app.persistence.repository import repository
        repository._storage = {}

    def tearDown(self):
        """Clean up after each test."""
        from app.persistence.repository import repository
        repository._storage = {}

    # User endpoint tests
    def test_create_user(self):
        """Test POST /api/v1/users/"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'password123',
                'first_name': 'John',
                'last_name': 'Doe'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['email'], 'test@example.com')
        self.assertNotIn('password', data)

    def test_get_user(self):
        """Test GET /api/v1/users/<user_id>"""
        # Create a user first
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'gettest@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertNotIn('password', data)

    def test_get_nonexistent_user(self):
        """Test GET /api/v1/users/<user_id> with invalid ID"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_list_users(self):
        """Test GET /api/v1/users/"""
        # Create multiple users
        self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'user2@example.com',
                'password': 'password456'
            }),
            content_type='application/json'
        )
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_update_user(self):
        """Test PUT /api/v1/users/<user_id>"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'update@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        
        # Update the user
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            data=json.dumps({
                'email': 'updated@example.com',
                'password': 'newpassword',
                'first_name': 'Updated',
                'last_name': 'User'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')

    # Amenity endpoint tests
    def test_create_amenity(self):
        """Test POST /api/v1/amenities/"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({
                'name': 'WiFi',
                'description': 'High-speed internet'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_get_amenity(self):
        """Test GET /api/v1/amenities/<amenity_id>"""
        # Create an amenity
        create_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'Pool'}),
            content_type='application/json'
        )
        amenity_id = json.loads(create_response.data)['id']
        
        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Pool')

    def test_list_amenities(self):
        """Test GET /api/v1/amenities/"""
        # Create amenities
        self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'Gym'}),
            content_type='application/json'
        )
        self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'Parking'}),
            content_type='application/json'
        )
        
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 2)

    def test_update_amenity(self):
        """Test PUT /api/v1/amenities/<amenity_id>"""
        # Create an amenity
        create_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'Old Name'}),
            content_type='application/json'
        )
        amenity_id = json.loads(create_response.data)['id']
        
        # Update the amenity
        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            data=json.dumps({
                'name': 'New Name',
                'description': 'Updated description'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Name')

    # Place endpoint tests
    def test_create_place(self):
        """Test POST /api/v1/places/"""
        # Create a user first
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        
        # Create a place
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'Beach House',
                'description': 'Beautiful beach view',
                'price': 200.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beach House')
        self.assertIn('owner', data)

    def test_create_place_with_invalid_owner(self):
        """Test POST /api/v1/places/ with invalid owner"""
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'House',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': 'invalid-owner'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_place(self):
        """Test GET /api/v1/places/<place_id>"""
        # Create user and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'Villa',
                'price': 300.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Villa')

    def test_list_places(self):
        """Test GET /api/v1/places/"""
        # Create user
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        
        # Create places
        for i in range(2):
            self.client.post(
                '/api/v1/places/',
                data=json.dumps({
                    'title': f'Place {i}',
                    'price': 100.0 + i,
                    'latitude': 0.0,
                    'longitude': 0.0,
                    'owner_id': owner_id
                }),
                content_type='application/json'
            )
        
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 2)

    # Review endpoint tests
    def test_create_review(self):
        """Test POST /api/v1/reviews/"""
        # Create user and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'reviewer@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'House',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        # Create review
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({
                'user_id': user_id,
                'place_id': place_id,
                'rating': 5,
                'text': 'Excellent place to stay!'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['rating'], 5)

    def test_get_review(self):
        """Test GET /api/v1/reviews/<review_id>"""
        # Create user, place, and review
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'House',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        review_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({
                'user_id': user_id,
                'place_id': place_id,
                'rating': 4,
                'text': 'Good place overall'
            }),
            content_type='application/json'
        )
        review_id = json.loads(review_response.data)['id']
        
        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['rating'], 4)

    def test_delete_review(self):
        """Test DELETE /api/v1/reviews/<review_id>"""
        # Create user, place, and review
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'House',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        review_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({
                'user_id': user_id,
                'place_id': place_id,
                'rating': 3,
                'text': 'Average experience'
            }),
            content_type='application/json'
        )
        review_id = json.loads(review_response.data)['id']
        
        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_place_reviews(self):
        """Test GET /api/v1/places/<place_id>/reviews"""
        # Create user and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'email': 'owner@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'House',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': owner_id
            }),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        # Create reviews
        for rating in [4, 5]:
            self.client.post(
                '/api/v1/reviews/',
                data=json.dumps({
                    'user_id': user_id,
                    'place_id': place_id,
                    'rating': rating,
                    'text': f'Rating {rating} review'
                }),
                content_type='application/json'
            )
        
        # Get place reviews
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)


if __name__ == "__main__":
    unittest.main()
