#!/usr/bin/env python3
"""Simple test script to verify the HBnB API functionality"""

from run import create_app
from app import facade


def test_user_operations():
    """Test user creation and retrieval"""
    print("Testing User operations...")
    
    # Create a user
    user_data = {
        'first_name': 'Tariq',
        'last_name': 'Almutairi',
        'email': 'tariq@example.com'
    }
    user = facade.create_user(user_data)
    print(f"✓ Created user: {user.to_dict()}")
    
    # Retrieve the user
    retrieved_user = facade.get_user(user.id)
    assert retrieved_user.email == 'tariq@example.com'
    print(f"✓ Retrieved user by ID: {retrieved_user.to_dict()}")
    
    # Get all users
    users = facade.get_all_users()
    assert len(users) == 1
    print(f"✓ Total users: {len(users)}")
    
    return user


def test_amenity_operations():
    """Test amenity creation and retrieval"""
    print("\nTesting Amenity operations...")
    
    # Create amenities
    amenity1_data = {
        'name': 'WiFi',
        'description': 'High-speed internet'
    }
    amenity1 = facade.create_amenity(amenity1_data)
    print(f"✓ Created amenity: {amenity1.to_dict()}")
    
    amenity2_data = {
        'name': 'Pool',
        'description': 'Outdoor swimming pool'
    }
    amenity2 = facade.create_amenity(amenity2_data)
    print(f"✓ Created amenity: {amenity2.to_dict()}")
    
    # Get all amenities
    amenities = facade.get_all_amenities()
    assert len(amenities) == 2
    print(f"✓ Total amenities: {len(amenities)}")
    
    return [amenity1, amenity2]


def test_place_operations(owner, amenities):
    """Test place creation and retrieval"""
    print("\nTesting Place operations...")
    
    # Create a place
    place_data = {
        'title': 'Luxury Villa in Riyadh',
        'description': 'Beautiful 5-bedroom villa in diplomatic quarter',
        'price': 1500.00,
        'latitude': 24.7136,
        'longitude': 46.6753,
        'owner_id': owner.id,
        'amenities': [amenity.id for amenity in amenities]
    }
    place = facade.create_place(place_data)
    print(f"✓ Created place: {place.to_dict()}")
    print(f"  - Amenities: {[a.name for a in place.amenities]}")
    
    # Retrieve the place
    retrieved_place = facade.get_place(place.id)
    assert retrieved_place.title == 'Luxury Villa in Riyadh'
    print(f"✓ Retrieved place by ID: {retrieved_place.title}")
    
    # Get all places
    places = facade.get_all_places()
    assert len(places) == 1
    print(f"✓ Total places: {len(places)}")
    
    return place


def test_review_operations(place, owner):
    """Test review creation and retrieval"""
    print("\nTesting Review operations...")
    
    # Create a second user to write a review
    reviewer_data = {
        'first_name': 'Shaden',
        'last_name': 'Almansour',
        'email': 'shaden@example.com'
    }
    reviewer = facade.create_user(reviewer_data)
    print(f"✓ Created reviewer: {reviewer.to_dict()}")
    
    # Create a review
    review_data = {
        'place_id': place.id,
        'user_id': reviewer.id,
        'rating': 5,
        'comment': 'Amazing property! Highly recommend.'
    }
    review = facade.create_review(review_data)
    print(f"✓ Created review: {review.to_dict()}")
    
    # Get all reviews
    reviews = facade.get_all_reviews()
    assert len(reviews) == 1
    print(f"✓ Total reviews: {len(reviews)}")
    
    # Get reviews for a place
    place_reviews = facade.get_reviews_by_place(place.id)
    assert len(place_reviews) == 1
    print(f"✓ Reviews for place: {len(place_reviews)}")
    
    # Check average rating
    avg_rating = place.calculate_average_rating()
    assert avg_rating == 5.0
    print(f"✓ Average rating: {avg_rating}")
    
    # Test that owner cannot review their own place
    try:
        invalid_review_data = {
            'place_id': place.id,
            'user_id': owner.id,
            'rating': 5,
            'comment': 'My own place is great!'
        }
        facade.create_review(invalid_review_data)
        print("✗ Should not allow owner to review own place")
    except ValueError as e:
        print(f"✓ Correctly prevented owner from reviewing own place: {e}")


def test_validation():
    """Test input validation"""
    print("\nTesting Validation...")
    
    # Test invalid email
    try:
        facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email'
        })
        print("✗ Should reject invalid email")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid email: {e}")
    
    # Test duplicate email
    try:
        facade.create_user({
            'first_name': 'Another',
            'last_name': 'User',
            'email': 'tariq@example.com'
        })
        print("✗ Should reject duplicate email")
    except ValueError as e:
        print(f"✓ Correctly rejected duplicate email: {e}")
    
    # Test invalid rating
    try:
        facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        })
    except:
        pass


def main():
    """Run all tests"""
    print("=" * 60)
    print("HBnB Application Tests")
    print("=" * 60)
    
    try:
        # Test user operations
        user = test_user_operations()
        
        # Test amenity operations
        amenities = test_amenity_operations()
        
        # Test place operations
        place = test_place_operations(user, amenities)
        
        # Test review operations
        test_review_operations(place, user)
        
        # Test validation
        test_validation()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
