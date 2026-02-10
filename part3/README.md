# HBnB Project - Part 3: Authentication & Database Integration

## � Project Overview

Part 3 extends the HBnB backend application by introducing **JWT-based authentication**, **role-based access control**, and **database integration** using **SQLAlchemy** with **SQLite** for development.

## 👥 Team Members

| Name | GitHub Username | Role |
|------|-----------------|------|
| Tariq Almutairi Rasheed Tariq | [@TariqRash](https://github.com/TariqRash) | Config, Repository, SQL Scripts, ER Diagram |
| Almansour Khaled Shaden | [@illo888](https://github.com/illo888) | User Model, Entity Mapping |
| Norah Mohammed Alskran | [@noneals](https://github.com/noneals) | JWT Auth, Endpoints, Relationships |

## 🎯 Objectives Achieved

- ✅ **JWT Authentication**: Secure login with Flask-JWT-Extended
- ✅ **Role-Based Access Control**: Admin vs regular user permissions
- ✅ **SQLAlchemy ORM**: Database persistence with SQLite
- ✅ **Entity Relationships**: One-to-many and many-to-many mappings
- ✅ **Password Hashing**: Secure bcrypt password storage
- ✅ **ER Diagram**: Database visualization with Mermaid.js

## 📁 Project Structure

```
part3/
├── app/
│   ├── __init__.py          # Application factory with extensions
│   ├── api/v1/
│   │   ├── auth.py          # Login endpoint
│   │   ├── users.py         # User CRUD endpoints
│   │   ├── places.py        # Place CRUD endpoints
│   │   ├── reviews.py       # Review CRUD endpoints
│   │   └── amenities.py     # Amenity CRUD endpoints
│   ├── models/
│   │   ├── base_model.py    # SQLAlchemy base with id, timestamps
│   │   ├── user.py          # User model with password hashing
│   │   ├── place.py         # Place model
│   │   ├── review.py        # Review model
│   │   ├── amenity.py       # Amenity model
│   │   └── associations.py  # Many-to-many junction table
│   ├── persistence/
│   │   └── sqlalchemy_repository.py  # Generic SQLAlchemy CRUD
│   └── services/
│       ├── facade.py        # Business logic facade
│       └── repositories/
│           └── user_repository.py    # User-specific queries
├── docs/
│   └── er_diagram.md        # Mermaid.js ER diagram
├── tests/
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   └── test_amenities.py
├── config.py                # Environment configurations
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── schema.sql               # SQL table definitions
└── seed.sql                 # Initial data (admin + amenities)
```

## 🔧 Task Completion

| Task | Description | Status |
|------|-------------|--------|
| 0 | Application Factory with Configuration | ✅ Complete |
| 1 | User Model with Password Hashing | ✅ Complete |
| 2 | JWT Authentication with flask-jwt-extended | ✅ Complete |
| 3 | Authenticated User Access Endpoints | ✅ Complete |
| 4 | Administrator Access Endpoints | ✅ Complete |
| 5 | SQLAlchemy Repository Implementation | ✅ Complete |
| 6 | Map User Entity to SQLAlchemy | ✅ Complete |
| 7 | Map Place, Review, Amenity Entities | ✅ Complete |
| 8 | Map Relationships Between Entities | ✅ Complete |
| 9 | SQL Scripts for Schema and Seed Data | ✅ Complete |
| 10 | ER Diagram with Mermaid.js | ✅ Complete |

## 🚀 Getting Started

### Installation

```bash
cd part3
pip install -r requirements.txt
```

### Running the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### API Documentation

Swagger docs available at: `http://localhost:5000/api/v1/docs`

## 🔐 Authentication

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin1234"}'
```

### Using JWT Token
```bash
curl -X GET http://localhost:5000/api/v1/users/ \
  -H "Authorization: Bearer <your_token>"
```

## 📊 API Endpoints

### Public Endpoints (No Auth Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/` | List all users |
| GET | `/api/v1/users/<id>` | Get user by ID |
| GET | `/api/v1/places/` | List all places |
| GET | `/api/v1/places/<id>` | Get place by ID |
| GET | `/api/v1/reviews/` | List all reviews |
| GET | `/api/v1/amenities/` | List all amenities |
| POST | `/api/v1/auth/login` | User login |

### Authenticated Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/places/` | Create place | User |
| PUT | `/api/v1/places/<id>` | Update place | Owner/Admin |
| DELETE | `/api/v1/places/<id>` | Delete place | Owner/Admin |
| POST | `/api/v1/reviews/` | Create review | User |
| PUT | `/api/v1/reviews/<id>` | Update review | Owner/Admin |
| DELETE | `/api/v1/reviews/<id>` | Delete review | Owner/Admin |

### Admin-Only Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create user |
| PUT | `/api/v1/users/<id>` | Update any user |
| POST | `/api/v1/amenities/` | Create amenity |
| PUT | `/api/v1/amenities/<id>` | Update amenity |

## 🗄️ Database Schema

### Entity Relationships
- **User → Places**: One-to-Many (user owns places)
- **User → Reviews**: One-to-Many (user writes reviews)
- **Place → Reviews**: One-to-Many (place has reviews)
- **Place ↔ Amenity**: Many-to-Many (via place_amenity table)

### ER Diagram
The complete Entity-Relationship diagram is available in `docs/er_diagram.md` using Mermaid.js syntax.

**To export as an image**: See `docs/EXPORT_DIAGRAM_INSTRUCTIONS.md` for detailed instructions on exporting the diagram to PNG/SVG format using Mermaid Live Editor, VS Code, or command-line tools.

### Initial Data
- **Admin User**: `admin@hbnb.io` / `admin1234`
- **Amenities**: WiFi, Swimming Pool, Air Conditioning

## 🔗 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- [Mermaid.js](https://mermaid-js.github.io/mermaid/)

---

> **Note**: This is Part 3 of the HBnB Project. See the main repository README for the complete project overview.
