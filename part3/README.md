You have exceeded your premium request allowance. We have automatically switched you to GPT-4.1 which is included with your plan. [Enable additional paid premium requests](command:chat.enablePremiumOverages) to continue using premium models.```markdown
# HBnB Project — Part 3: Authentication & Database

## 📚 Introduction
Part 3 upgrades the HBnB backend with:
- Secure user authentication (JWT)
- Role-based access (admin/user)
- Persistent storage using SQLAlchemy (SQLite/MySQL)
- Full entity relationships and ERD

This part builds on previous work (Parts 1 & 2) and prepares the app for real-world deployment.

---

## 👥 Team

| Name                        | Role                        | Responsibilities                                  |
|-----------------------------|-----------------------------|---------------------------------------------------|
| Tariq Rashed Almutairi      | Business Logic & DB Schema  | Models, relationships, SQL, ERD                   |
| Almansour Khaled Shaden     | API & Auth                  | Endpoints, JWT, RBAC, seed data, docs             |
| Norah Mohammed Alskran      | Testing & Documentation     | Testing, validation, SQL scripts, final docs      |

---

## 🚀 Features
- JWT authentication & session management
- Role-based access control (is_admin)
- Secure password hashing (bcrypt)
- CRUD for User, Place, Review, Amenity
- Ownership & admin permissions
- SQLAlchemy ORM (SQLite for dev, MySQL for prod)
- ER diagram (Mermaid.js)
- SQL scripts for schema & seed data

---

## 🗂️ Project Structure

```
part3/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   │       └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   │   └── repositories/
│   │       ├── user_repository.py
│   │       ├── place_repository.py
│   │       ├── review_repository.py
│   │       └── amenity_repository.py
│   └── persistence/
│       ├── __init__.py
│       └── sqlalchemy_repository.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   ├── test_amenities.py
│   └── test_validation.py
├── docs/
│   └── er_diagram.md
├── part3/
│   ├── schema.sql
│   ├── seed.sql
│   └── README.md
├── requirements.txt
├── run.py
└── README.md
```

---

## 📝 Tasks Overview

- **Task 0:** Application Factory & Config
- **Task 1:** User Model & Password Hashing
- **Task 2:** JWT Authentication & Login Endpoint
- **Task 3:** Authenticated User Access Endpoints
- **Task 4:** Admin Access & RBAC
- **Task 5:** SQLAlchemy Repository & Facade
- **Task 6:** Map User Entity to SQLAlchemy Model
- **Task 7:** Map Place, Review, Amenity Entities
- **Task 8:** Map Relationships Between Entities
- **Task 9:** SQL Scripts for Table Generation & Initial Data
- **Task 10:** Generate Database Diagrams (Mermaid.js ERD)

---

## ⚡ How to Run

```bash
git clone https://github.com/TariqRash/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
pip install -r requirements.txt
python run.py
# Swagger: http://localhost:5000/api/v1/doc
```

---

## 🧪 Testing

```bash
python -m unittest discover -s tests -p "test_*.py"
# or
python -m pytest tests -v
```

---

## 🗃️ Database

- **Development:** SQLite (default)
- **Production:** MySQL (configurable)
- **Schema & Seed:** See `part3/schema.sql` and `part3/seed.sql`
- **ER Diagram:** See `docs/er_diagram.md`

---

## 📄 References

- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Mermaid.js](https://mermaid-js.github.io/mermaid/)

---
هذا هو ملف README.md شامل وجاهز للرفع والتقييم لبارت 3.
