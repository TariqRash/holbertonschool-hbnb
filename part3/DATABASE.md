# Database Setup Instructions

This directory contains SQL scripts to set up the HBnB application database with sample data.

## Files

- **`schema.sql`**: Database schema (table definitions, indexes, relationships)
- **`seed.sql`**: Sample data (users, places, amenities, reviews)

## Quick Setup

### Option 1: Automatic Setup (Python)
The application will automatically create the database when you run it for the first time:

```bash
python3 run.py
```

If you want to start fresh with sample data:

```bash
# Remove old database
rm -f instance/development.db

# Create instance directory if it doesn't exist
mkdir -p instance

# Run the application (creates tables automatically)
python3 run.py
```

Then populate with sample data using the Flask shell:

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

# Load sample data
sqlite3 instance/development.db < seed.sql
```

### Option 2: Manual Setup (SQLite)
If you want to manually set up the database:

```bash
# Create instance directory
mkdir -p instance

# Create database with schema
sqlite3 instance/development.db < schema.sql

# Load sample data
sqlite3 instance/development.db < seed.sql
```

## Sample Data Included

### Users (5 total)
- **Admin HBnB** (admin@hbnb.io) - Administrator account
  - Password: `admin1234`
- **John Doe** (john@example.com) - Regular user
  - Password: `123456`
- Additional test users

### Places (4 total)
- Cozy Beach House
- Modern City Apartment
- Mountain Retreat
- Luxury Downtown Loft

### Amenities (4 total)
- WiFi
- Swimming Pool
- Air Conditioning
- Parking

### Reviews (4 total)
- Sample reviews from users for various places

## Verification

To verify the database was set up correctly:

```bash
sqlite3 instance/development.db "SELECT COUNT(*) as user_count FROM users;"
sqlite3 instance/development.db "SELECT COUNT(*) as place_count FROM places;"
sqlite3 instance/development.db "SELECT COUNT(*) as amenity_count FROM amenities;"
sqlite3 instance/development.db "SELECT COUNT(*) as review_count FROM reviews;"
```

Expected output:
- Users: 5
- Places: 4
- Amenities: 4
- Reviews: 4

## Login Credentials

### Admin Account
- Email: `admin@hbnb.io`
- Password: `admin1234`

### Test User Account
- Email: `john@example.com`
- Password: `123456`

## Resetting the Database

To start fresh:

```bash
# Remove the database
rm -f instance/development.db

# Recreate with schema and sample data
sqlite3 instance/development.db < schema.sql
sqlite3 instance/development.db < seed.sql
```

## Notes

- The database file (`instance/development.db`) is excluded from git via `.gitignore`
- These SQL scripts ensure consistent sample data across all devices
- The schema matches the SQLAlchemy models defined in `app/models/`
- All passwords are hashed using bcrypt for security
