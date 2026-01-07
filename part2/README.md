# Part 2: Implementation of Business Logic and API Endpoints

This directory contains the implementation of the HBnB application with a three-layer architecture using Python and Flask.

## Project Structure

```
part2/
├── app/
│   ├── __init__.py
│   ├── models/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── base_entity.py     # Abstract base class
│   │   ├── user.py            # User entity
│   │   ├── place.py           # Place entity
│   │   ├── review.py          # Review entity
│   │   └── amenity.py         # Amenity entity
│   ├── persistence/            # Persistence Layer
│   │   ├── __init__.py
│   │   └── repository.py      # In-memory repository
│   ├── services/               # Facade Pattern
│   │   ├── __init__.py
│   │   └── facade.py          # HBnBFacade
│   └── api/                    # Presentation Layer
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── users.py       # User endpoints
│           ├── places.py      # Place endpoints
│           ├── reviews.py     # Review endpoints
│           └── amenities.py   # Amenity endpoints
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Architecture

### Three-Layer Architecture

1. **Presentation Layer** (`app/api/`): RESTful API endpoints using Flask-RESTX
2. **Business Logic Layer** (`app/models/`): Core domain models and business rules
3. **Persistence Layer** (`app/persistence/`): Data storage using in-memory repository

### Facade Pattern

The `HBnBFacade` class in `app/services/facade.py` provides a unified interface between the Presentation and Business Logic layers, simplifying communication and reducing coupling.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Navigate to the part2 directory:
```bash
cd part2
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask development server:

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## API Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) at:

```
http://localhost:5000/api/v1/docs
```

This interactive documentation allows you to:
- Explore all available endpoints
- View request/response schemas
- Test API calls directly from your browser

## API Endpoints

### Users
- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user

### Places
- `GET /api/v1/places` - List all places (with owner and amenities details)
- `POST /api/v1/places` - Create a new place
- `GET /api/v1/places/{place_id}` - Get a specific place (with owner and amenities details)
- `PUT /api/v1/places/{place_id}` - Update a place

### Reviews
- `GET /api/v1/reviews` - List all reviews (with user and place details)
- `POST /api/v1/reviews` - Create a new review
- `GET /api/v1/reviews/{review_id}` - Get a specific review (with user and place details)
- `PUT /api/v1/reviews/{review_id}` - Update a review
- `DELETE /api/v1/reviews/{review_id}` - Delete a review
- `GET /api/v1/reviews/places/{place_id}` - Get all reviews for a specific place

### Amenities
- `GET /api/v1/amenities` - List all amenities
- `POST /api/v1/amenities` - Create a new amenity
- `GET /api/v1/amenities/{amenity_id}` - Get a specific amenity
- `PUT /api/v1/amenities/{amenity_id}` - Update an amenity

## Data Serialization

The API implements data serialization with extended attributes for related objects:

- **Place endpoints** include:
  - Owner details (first_name, last_name, email)
  - Amenities list with names
  
- **Review endpoints** include:
  - User details (first_name, last_name)
  - Place details (title)

## Example Usage

### Create a User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Tariq",
    "last_name": "Almutairi",
    "email": "tariq@example.com"
  }'
```

### Create a Place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Luxury Villa in Riyadh",
    "description": "Beautiful villa in diplomatic quarter",
    "price": 1500.00,
    "latitude": 24.7136,
    "longitude": 46.6753,
    "owner_id": "{user_id}"
  }'
```

### Create a Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "place_id": "{place_id}",
    "user_id": "{user_id}",
    "rating": 5,
    "comment": "Amazing property!"
  }'
```

## Business Rules and Validations

### User
- First and last names: 2-50 characters
- Email must be unique and valid format
- Cannot have duplicate email addresses

### Place
- Title: 5-100 characters
- Description: Required, max 1000 characters
- Price: Must be positive
- Latitude: -90 to 90
- Longitude: -180 to 180
- Must have a valid owner

### Review
- Rating: Integer between 1-5
- Comment: Required, max 500 characters
- User cannot review their own place

### Amenity
- Name: 3-50 characters, must be unique
- Description: Optional, max 200 characters

## Design Patterns Used

1. **Facade Pattern**: Simplifies communication between layers
2. **Repository Pattern**: Abstracts data access logic
3. **Template Method Pattern**: BaseEntity provides common structure

## Future Enhancements (Part 3)

- Database integration using SQLAlchemy
- JWT authentication
- Role-based access control
- Advanced search and filtering
- Pagination support

## Team

- **Tariq Rashed Almutairi** - tariq@hostworksa.com
- **Shaden Khaled Almansour** - shadeenn1424@gmail.com
- **Nora Mohammed Alsakran** - none.als012@gmail.com

**Organization:** Holberton School Saudi Arabia  
**Project:** HBnB Evolution - Part 2  
**Date:** December 2025
