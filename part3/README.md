# HBnB Evolution

A comprehensive AirBnB-like backend application demonstrating enterprise-grade software architecture, authentication, and database persistence.

---

## 🎯 Project Overview

This project is part of **Holberton School – Advanced Backend Specialization** and showcases:

- Layered Architecture (Presentation / Business Logic / Persistence)
- Design Patterns (Facade, Repository)
- JWT Authentication & Role-Based Access Control
- SQLAlchemy ORM with relational database modeling
- Clean, scalable RESTful API design

---

# HBnB Project — Part 3: Authentication & Database

## 📚 Introduction

Part 3 upgrades the HBnB backend by adding:

- Secure JWT-based authentication
- Role-based access control (admin vs user)
- Persistent storage using SQLAlchemy
- Full entity relationships
- SQL schema & seed scripts
- Entity Relationship Diagram (ERD)

This part builds on **Part 1 (Design)** and **Part 2 (Core Logic)**.

---

## 👥 Team

| Name | Role | Responsibilities |
|-----|-----|------------------|
| Tariq Rashed Almutairi | Project Lead | Models, DB schema, ERD |
| Shaden Khaled Almansour | API & Auth | Endpoints, JWT, RBAC |
| Norah Mohammed Alskran | Testing & Docs | Tests, validation, SQL |

---

## 🚀 Features

- JWT authentication (Flask-JWT-Extended)
- Secure password hashing (bcrypt)
- Admin & user roles
- CRUD operations for:
  - Users
  - Places
  - Reviews
  - Amenities
- Ownership & permission enforcement
- SQLAlchemy ORM (SQLite for dev)
- ER Diagram using Mermaid.js
- SQL schema & seed data

---

## 🗂️ Project Structure
part3/
├── app/
│ ├── init.py
│ ├── models/
│ │ ├── base_model.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ ├── amenity.py
│ │ └── associations.py
│ ├── api/
│ │ └── v1/
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ ├── amenities.py
│ │ └── auth.py
│ ├── services/
│ │ └── facade.py
│ └── persistence/
│ └── sqlalchemy_repository.py
├── tests/
│ ├── test_users.py
│ ├── test_places.py
│ ├── test_reviews.py
│ └── test_amenities.py
├── docs/
│ └── er_diagram.md
├── schema.sql
├── seed.sql
├── config.py
├── requirements.txt
└── README.md


---

## 📝 Tasks Overview

- **Task 0:** Application Factory & Config
- **Task 1:** User Model & Password Hashing
- **Task 2:** JWT Authentication
- **Task 3:** Authenticated User Endpoints
- **Task 4:** Admin Access & RBAC
- **Task 5:** SQLAlchemy Repository
- **Task 6:** Map User Entity
- **Task 7:** Map Place, Review, Amenity Entities
- **Task 8:** Entity Relationships
- **Task 9:** SQL Schema & Seed Data
- **Task 10:** ER Diagram (Mermaid.js)

---

## ⚡ How to Run

```bash
git clone https://github.com/<your-repo>/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
pip install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development
flask run


📄 Swagger UI:

http://localhost:5000/api/v1/docs

🧪 Testing
python -m unittest discover -s tests -p "test_*.py"

🗃️ Database

Development: SQLite

Testing: In-memory SQLite

Production-ready: MySQL-compatible

Files:

schema.sql – table definitions

seed.sql – initial data

docs/er_diagram.md – ER diagram (Mermaid)

📚 References

Flask-JWT-Extended
https://flask-jwt-extended.readthedocs.io/

Flask-Bcrypt
https://flask-bcrypt.readthedocs.io/

SQLAlchemy
https://docs.sqlalchemy.org/

Mermaid.js
https://mermaid-js.github.io/

📌 Notes

All code is written in English (ASCII)

Repository & Facade patterns are enforced

Database relationships are fully normalized

No plaintext passwords stored

Compatible with Parts 1 & 2 design

🎓 Academic Context

School: Holberton School Saudi Arabia
Program: Advanced Backend Specialization
Project: HBnB Evolution – Part 3
Year: 2026
