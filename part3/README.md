# HBnB Project — Part 3: Authentication & Database

## 📚 Introduction
Part 3 upgrades the HBnB backend with:
- Secure user authentication (JWT)
- Role-based access (admin/user)
- Persistent storage using SQLAlchemy (SQLite/MySQL)
- Full entity relationships and ERD

This part builds on previous work (Parts 1 & 2) and prepares the app for real-world deployment.

## 🚀 Features
- JWT authentication & session management
- Role-based access control (is_admin)
- Secure password hashing (bcrypt)
- CRUD for User, Place, Review, Amenity
- Ownership & admin permissions
- SQLAlchemy ORM (SQLite for dev, MySQL for prod)
- ER diagram (Mermaid.js)
- SQL scripts for schema & seed data

## 🗂️ Project Structure
- `app/models/` — SQLAlchemy models (User, Place, Review, Amenity)
- `app/api/v1/` — API endpoints (users, places, reviews, amenities, auth)
- `app/services/` — Facade & repositories (business logic)
- `app/persistence/` — SQLAlchemy repository
- `tests/` — Unit & integration tests
- `docs/` — ER diagrams & documentation
- `schema.sql` / `seed.sql` — SQL scripts for DB schema & initial data

## ⚙️ Setup & Usage
1. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
2. Initialize the database:
	```bash
	flask shell
	>>> from app import db
	>>> db.create_all()
	```
3. Run the app:
	```bash
	flask run
	# or
	python run.py
	```
4. Run tests:
	```bash
	python -m unittest discover tests
	```

## 👥 Team Responsibilities
- **Tariq:** Models, DB schema, ER diagram, relationships
- **Shaden:** API endpoints, Auth, RBAC, seed data, docs
- **Nora:** Testing, validation, SQL scripts, documentation
