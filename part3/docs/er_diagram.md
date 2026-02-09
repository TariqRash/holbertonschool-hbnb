# HBnB Database Entity-Relationship Diagram

This document contains the ER diagram for the HBnB application database schema using Mermaid.js syntax.

## ER Diagram

```mermaid
erDiagram
    USERS {
        char(36) id PK "UUID Primary Key"
        varchar(255) first_name "NOT NULL"
        varchar(255) last_name "NOT NULL"
        varchar(255) email "UNIQUE, NOT NULL"
        varchar(255) password "NOT NULL (bcrypt hashed)"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "DEFAULT CURRENT_TIMESTAMP"
    }

    PLACES {
        char(36) id PK "UUID Primary Key"
        varchar(255) title "NOT NULL"
        text description
        decimal(10_2) price "NOT NULL, CHECK > 0"
        float latitude "NOT NULL, CHECK -90 to 90"
        float longitude "NOT NULL, CHECK -180 to 180"
        char(36) owner_id FK "References users(id)"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "DEFAULT CURRENT_TIMESTAMP"
    }

    REVIEWS {
        char(36) id PK "UUID Primary Key"
        text text "NOT NULL"
        int rating "NOT NULL, CHECK 1-5"
        char(36) user_id FK "References users(id)"
        char(36) place_id FK "References places(id)"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "DEFAULT CURRENT_TIMESTAMP"
    }

    AMENITIES {
        char(36) id PK "UUID Primary Key"
        varchar(255) name "UNIQUE, NOT NULL"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "DEFAULT CURRENT_TIMESTAMP"
    }

    PLACE_AMENITY {
        char(36) place_id PK_FK "References places(id)"
        char(36) amenity_id PK_FK "References amenities(id)"
    }

    USERS ||--o{ PLACES : "owns (one-to-many)"
    USERS ||--o{ REVIEWS : "writes (one-to-many)"
    PLACES ||--o{ REVIEWS : "has (one-to-many)"
    PLACES }o--o{ AMENITIES : "has (many-to-many)"
    PLACES ||--o{ PLACE_AMENITY : "links"
    AMENITIES ||--o{ PLACE_AMENITY : "links"
```

## Relationships Explained

### One-to-Many Relationships:
1. **User → Places**: A user can own multiple places. Each place has exactly one owner.
2. **User → Reviews**: A user can write multiple reviews. Each review is written by exactly one user.
3. **Place → Reviews**: A place can have multiple reviews. Each review belongs to exactly one place.

### Many-to-Many Relationships:
1. **Place ↔ Amenity**: A place can have multiple amenities, and an amenity can belong to multiple places. This is implemented via the `place_amenity` junction table.

## Constraints

- **Unique Constraint**: `(user_id, place_id)` in Reviews table - ensures a user can only review a place once.
- **Foreign Key Constraints**: All foreign keys have `ON DELETE CASCADE` to maintain referential integrity.
- **Check Constraints**: 
  - `rating` must be between 1 and 5
  - `price` must be greater than 0
  - `latitude` must be between -90 and 90
  - `longitude` must be between -180 and 180
