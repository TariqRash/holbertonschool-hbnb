# Part 1: Technical Documentation

## Overview

This directory contains the complete technical documentation for the HBnB Evolution project's architecture and design. Part 1 focuses on establishing a solid foundation through comprehensive UML modeling and architectural planning.

## 📋 Contents

### Task 0: High-Level Package Diagram
**File:** [`package-diagram.md`](./package-diagram.md)  
**Responsible:** Shaden Khaled Almansour  
**Description:** Illustrates the three-layer architecture (Presentation, Business Logic, Persistence) and demonstrates how the Facade pattern facilitates communication between layers.

### Task 1: Detailed Class Diagram
**File:** [`class-diagram.md`](./class-diagram.md)  
**Responsible:** Tariq Rashed Almutairi  
**Description:** Comprehensive class diagram for the Business Logic layer, depicting all entities (User, Place, Review, Amenity), their attributes, methods, and relationships following SOLID principles.

### Task 2: Sequence Diagrams for API Calls
**File:** [`sequence-diagrams.md`](./sequence-diagrams.md)  
**Responsible:** Nora Mohammed Alsakran  
**Description:** Four detailed sequence diagrams showing the complete interaction flow for critical API operations:
- User Registration
- Place Creation
- Review Submission
- Fetching List of Places

### Task 3: Compiled Technical Documentation
**File:** `technical-documentation.pdf`  
**Responsible:** Team Collaboration  
**Description:** Professional PDF compilation of all diagrams and technical specifications with comprehensive explanatory notes.

## 🏗️ Architecture Overview

### Three-Layer Architecture
```
┌─────────────────────────────────────────┐
│     Presentation Layer                  │
│     - API Endpoints (REST)              │
│     - Request/Response Handling         │
│     - Authentication & Authorization    │
└──────────────┬──────────────────────────┘
               │
               │ Facade Pattern Interface
               │
┌──────────────▼──────────────────────────┐
│     Business Logic Layer                │
│     - Domain Models (Entities)          │
│     - Business Rules & Validation       │
│     - Core Application Logic            │
└──────────────┬──────────────────────────┘
               │
               │ Repository Pattern
               │
┌──────────────▼──────────────────────────┐
│     Persistence Layer                   │
│     - Database Operations               │
│     - Data Access Objects (DAO)         │
│     - ORM Mappings                      │
└─────────────────────────────────────────┘
```

### Design Patterns

1. **Facade Pattern**: Provides a unified interface to the Business Logic layer
2. **Repository Pattern**: Abstracts data persistence operations
3. **MVC Pattern**: Separates concerns in the presentation layer

## 🎯 Core Business Entities

### User Entity
- Manages user accounts and authentication
- Supports both regular users and administrators

### Place Entity
- Represents property listings with location and pricing
- Supports multiple amenities

### Review Entity
- User-generated feedback with ratings (1-5 scale)

### Amenity Entity
- Reusable features for places (WiFi, Pool, etc.)

## 🔄 Entity Relationships

- **User → Place**: One-to-Many
- **User → Review**: One-to-Many
- **Place → Review**: One-to-Many
- **Place ↔ Amenity**: Many-to-Many

## 📐 UML Standards

All diagrams follow:
- UML 2.5 Notation
- Mermaid.js Syntax (GitHub rendering)
- Professional documentation standards

## 👥 Team Contact

| Name | Role | Email |
|------|------|-------|
| Tariq Rashed Almutairi | Project Lead & Class Diagram | Tariq@hostworksa.com |
| Shaden Khaled Almansour | Package Architecture | shadeenn1424@gmail.com |
| Nora Mohammed Alsakran | Sequence Diagrams | NoraAlsakran1122@gmail.com |

**Organization:** Holberton School Saudi Arabia  
**Location:** Riyadh, Saudi Arabia

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Status:** In Development
