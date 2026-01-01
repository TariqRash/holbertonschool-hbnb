# HBnB Evolution - Part 2 (BL & API)

Implementation of Business Logic and API Endpoints using Python, Flask, and flask-restx.

## Overview
- Build Presentation and Business Logic layers based on Part 1 design.
- Focus on core CRUD for User, Place, Amenity, Review (DELETE only for Review).
- In-memory repository for now (DB comes in Part 3).
- Facade pattern to connect API and business logic.

## Team
| Name | Role | Responsibilities |
|------|------|------------------|
| Tariq Rashed Almutairi | Business Logic | Models, validation, relationships |
| Almansour Khaled Shaden | API/Presentation | Endpoints, swagger, serialization |
| Norah Mohammed Alskran | QA & Testing | Unit tests, validation checks, reports |

## Repository & References
- Repo: https://github.com/TariqRash/holbertonschool-hbnb (branch: main)
- Path: `part2/`
- Reference docs: `holpRefrence/` (detailed task instructions provided by the school)

## Project Structure
```
part2/
├── app/
│   ├── __init__.py                 # Flask app wiring + namespaces
│   ├── models/                     # Business Logic layer
│   │   ├── __init__.py
│   │   ├── base_model.py           # BaseModel (id, created_at, updated_at)
│   │   ├── user.py                 # User
│   │   ├── amenity.py              # Amenity
│   │   ├── place.py                # Place
│   │   └── review.py               # Review
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py               # Facade to repository and models
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py            # User endpoints
│   │       ├── amenities.py        # Amenity endpoints
│   │       ├── places.py           # Place endpoints
│   │       └── reviews.py          # Review endpoints
│   └── persistence/
│       ├── __init__.py
│       └── repository.py           # In-memory repository
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_amenities.py
│   ├── test_places.py
│   └── test_reviews.py
├── requirements.txt
├── run.py
└── README.md                       # This file
```

## Tasks (what to implement)
0) Project Setup & Package Init
- Scaffold folders/packages for Presentation, Business Logic, Persistence.
- Provide in-memory repository and wire Facade.

1) Core Business Logic Classes (Tariq)
- Implement models: User, Place, Review, Amenity (+ BaseModel).
- Add validation methods and relationships (place-owner, place-amenities, place-reviews).

2) User Endpoints (Shaden)
- POST/GET list/GET by id/PUT (no DELETE).
- Do not return password in responses.

3) Amenity Endpoints (Shaden)
- POST/GET list/GET by id/PUT (no DELETE).

4) Place Endpoints (Shaden)
- POST/GET list/GET by id/PUT (no DELETE).
- Include owner info and amenities in responses; validate price/lat/lng.

5) Review Endpoints (Shaden)
- POST/GET list/GET by id/PUT/DELETE (DELETE only entity allowed).
- Ensure review ties to user and place; surfaces in place reviews list.

6) Testing & Validation (Norah)
- Validation coverage for all models.
- Black-box testing via curl/Postman and swagger UI.
- Unit tests (pytest/unittest) for all endpoints.
- Document test results and edge cases.

## API Surface (v1)
- Users: `GET /api/v1/users/`, `POST /`, `GET /<id>`, `PUT /<id>`
- Amenities: `GET /api/v1/amenities/`, `POST /`, `GET /<id>`, `PUT /<id>`
- Places: `GET /api/v1/places/`, `POST /`, `GET /<id>`, `PUT /<id>`, `GET /<id>/reviews`
- Reviews: `GET /api/v1/reviews/`, `POST /`, `GET /<id>`, `PUT /<id>`, `DELETE /<id>`

## Setup
```bash
git clone https://github.com/TariqRash/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
pip install -r requirements.txt
python run.py
# swagger: http://localhost:5000/api/v1/doc
```

## Testing
```bash
python -m unittest discover -s tests -p "test_*.py"
# or
python -m pytest tests -v
```

## Notes
- In-memory storage is temporary; DB integration comes in Part 3.
- Keep code ASCII/English only.
- Detailed school instructions are stored in `holpRefrence/` (reference only, do not modify).
