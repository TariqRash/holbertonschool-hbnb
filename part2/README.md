# HBnB Evolution - Part 2: Implementation

Implementation of Business Logic and API Endpoints for the HBnB Evolution platform.

## 🎯 Project Overview

Part 2 focuses on bringing the documented architecture to life through well-structured code. This phase implements:
- **Business Logic Layer** - Core models (User, Place, Review, Amenity)
- **Presentation Layer** - RESTful API with Flask and flask-restx
- **Persistence Layer** - In-Memory Repository (temporary, replaced in Part 3)
- **Facade Pattern** - Simplified communication between layers

## 👥 Team

| Name | Role | Responsibilities |
|------|------|------------------|
| **Tariq Rashed Almutairi** | Business Logic Developer | Models, Validation, Data Structures |
| **Shaden Khaled Almansour** | API Developer | Endpoints, Services, Swagger Documentation |
| **Nora Mohammed Alsakran** | QA & Testing Lead | Unit Tests, Validation Testing, Documentation |

**Organization:** Holberton School Saudi Arabia  
**Location:** Riyadh, Saudi Arabia 🇸🇦

## 📁 Project Structure

```
part2/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py          # BaseModel (UUID, timestamps)
│   │   ├── user.py                # User model
│   │   ├── amenity.py             # Amenity model
│   │   ├── place.py               # Place model
│   │   └── review.py              # Review model
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py              # Facade pattern implementation
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py           # User endpoints
│   │       ├── amenities.py       # Amenity endpoints
│   │       ├── places.py          # Place endpoints
│   │       └── reviews.py         # Review endpoints
│   └── persistence/
│       ├── __init__.py
│       └── repository.py          # In-Memory repository
├── tests/
│   ├── __init__.py
│   ├── test_users.py              # User tests
│   ├── test_amenities.py          # Amenity tests
│   ├── test_places.py             # Place tests
│   └── test_reviews.py            # Review tests
├── requirements.txt               # Python dependencies
├── run.py                         # Application entry point
└── README.md                      # This file
```

## 🚀 Features Implemented

### Core Models (Business Logic)
- ✅ **BaseModel** - Common attributes (id, created_at, updated_at)
- ✅ **User** - User management with validation
- ✅ **Amenity** - Property amenities
- ✅ **Place** - Property listings with owner/amenities relationships
- ✅ **Review** - User reviews with ratings (1-5)

### API Endpoints

#### Users (`/api/v1/users/`)
- `GET /` - List all users
- `POST /` - Create new user
- `GET /<user_id>` - Get user by ID
- `PUT /<user_id>` - Update user

#### Amenities (`/api/v1/amenities/`)
- `GET /` - List all amenities
- `POST /` - Create new amenity
- `GET /<amenity_id>` - Get amenity by ID
- `PUT /<amenity_id>` - Update amenity

#### Places (`/api/v1/places/`)
- `GET /` - List all places
- `POST /` - Create new place
- `GET /<place_id>` - Get place by ID
- `PUT /<place_id>` - Update place
- `GET /<place_id>/reviews` - Get reviews for a place

#### Reviews (`/api/v1/reviews/`)
- `GET /` - List all reviews
- `POST /` - Create new review
- `GET /<review_id>` - Get review by ID
- `PUT /<review_id>` - Update review
- `DELETE /<review_id>` - Delete review ⭐ (Only entity with DELETE)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/TariqRash/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Swagger Documentation
Access interactive API documentation at: `http://localhost:5000/api/v1/doc`

## 🧪 Testing

### Run all tests:
```bash
python run_tests.py
```

### Run specific test file:
```bash
python -m pytest tests/test_users.py -v
```

### Test with unittest:
```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## 🔧 Technologies

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.x |
| **Framework** | Flask 2.3.0 |
| **API Documentation** | flask-restx 0.5.1 |
| **Testing** | pytest 7.4.0, unittest |
| **Data Storage** | In-Memory Repository (temporary) |
| **Version Control** | Git & GitHub |

## 📝 Key Design Patterns

### 1. **Facade Pattern**
- Simplifies communication between Presentation and Business Logic layers
- Located in `app/services/facade.py`

### 2. **Repository Pattern**
- Abstracts data persistence operations
- In-Memory implementation in `app/persistence/repository.py`

### 3. **MVC Pattern**
- Models: `app/models/`
- Views/Controllers: `app/api/v1/`
- Separation of concerns maintained

## ✅ Task Distribution

| Task | Owner | Status |
|------|-------|--------|
| **Task 0:** Project Setup | Team | ✅ Complete |
| **Task 1:** Business Logic Classes | Tariq | ✅ Complete |
| **Task 2:** User Endpoints | Shaden | ✅ Complete |
| **Task 3:** Amenity Endpoints | Shaden | ✅ Complete |
| **Task 4:** Place Endpoints | Shaden | ✅ Complete |
| **Task 5:** Review Endpoints | Shaden | ✅ Complete |
| **Task 6:** Testing & Validation | Nora | ✅ Complete |

## 📚 API Usage Examples

### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Create Place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Apartment",
    "description": "A lovely apartment",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "{user_id}"
  }'
```

### Create Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "place_id": "{place_id}",
    "user_id": "{user_id}",
    "rating": 5,
    "comment": "Excellent place!"
  }'
```

## 🔄 Development Workflow

1. **Branch Strategy:**
   - `main` - Production-ready code
   - `dev` - Development branch
   - `feature/*` - Feature branches

2. **Commit Convention:**
   - `Add:` - New features
   - `Fix:` - Bug fixes
   - `Update:` - Updates to existing features
   - `Test:` - Test additions/updates

3. **Pull Request Process:**
   - Create feature branch
   - Implement changes
   - Run tests
   - Create PR for review
   - Merge after approval

## 🎓 Academic Context

**School:** Holberton School Saudi Arabia  
**Program:** Advanced Backend Specialization  
**Project:** HBnB Evolution - Part 2  
**Date:** January 2026

## 📄 License

© 2026 Holberton School Saudi Arabia. All rights reserved.

## 🔗 Related Documentation

- Part 1: Technical Documentation
- [API Documentation](http://localhost:5000/api/v1/doc) (when running)
- [Project Repository](https://github.com/TariqRash/holbertonschool-hbnb)

---

**Next Phase:** Part 3 - Database Integration with SQLAlchemy
