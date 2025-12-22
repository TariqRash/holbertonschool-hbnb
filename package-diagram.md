# Task 0: High-Level Package Diagram

## Overview
This diagram illustrates the three-layer architecture of the HBnB Evolution application, demonstrating the separation of concerns and communication patterns between layers using the Facade design pattern.

## Architecture Layers

### 1. Presentation Layer (Services & API)
- **Responsibility**: Handles all user interactions and HTTP requests
- **Components**: RESTful API endpoints, Request/Response handlers
- **Communication**: Interacts with Business Logic via Facade pattern

### 2. Business Logic Layer (Models)
- **Responsibility**: Contains core business rules and domain models
- **Components**: Entity models (User, Place, Review, Amenity), Business rules validation
- **Communication**: Receives requests from Presentation, communicates with Persistence

### 3. Persistence Layer (Database)
- **Responsibility**: Manages data storage and retrieval
- **Components**: Database operations, Data access objects, ORM mappings
- **Communication**: Provides data to Business Logic layer

## Facade Pattern Implementation
The Facade pattern provides a unified interface that:
- Simplifies communication between layers
- Reduces coupling and dependencies
- Centralizes business logic access
- Improves maintainability and testability

## Package Diagram

```mermaid
graph TB
    subgraph Presentation["🎨 Presentation Layer"]
        API[API Services]
        Routes[Route Handlers]
        Controllers[Controllers]
    end
    
    subgraph Business["⚙️ Business Logic Layer"]
        Facade[Facade Pattern Interface]
        Models[Domain Models]
        User[User Model]
        Place[Place Model]
        Review[Review Model]
        Amenity[Amenity Model]
    end
    
    subgraph Persistence["💾 Persistence Layer"]
        Repository[Repository Pattern]
        Database[(Database)]
        ORM[ORM/Data Mappers]
    end
    
    %% Connections
    API --> Facade
    Routes --> Facade
    Controllers --> Facade
    
    Facade --> Models
    Models --> User
    Models --> Place
    Models --> Review
    Models --> Amenity
    
    User --> Repository
    Place --> Repository
    Review --> Repository
    Amenity --> Repository
    
    Repository --> ORM
    ORM --> Database
    
    %% Styling
    classDef presentationStyle fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef businessStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef persistenceStyle fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class API,Routes,Controllers presentationStyle
    class Facade,Models,User,Place,Review,Amenity businessStyle
    class Repository,Database,ORM persistenceStyle
```

## Alternative Detailed Package Diagram

```mermaid
classDiagram
    namespace PresentationLayer {
        class APIServices {
            <<Interface>>
            +handle_request()
            +send_response()
        }
        class Controllers {
            +UserController
            +PlaceController
            +ReviewController
            +AmenityController
        }
    }
    
    namespace BusinessLogicLayer {
        class Facade {
            <<Interface>>
            +create_user()
            +create_place()
            +create_review()
            +create_amenity()
            +get_entity()
            +update_entity()
            +delete_entity()
        }
        class Models {
            +User
            +Place
            +Review
            +Amenity
        }
    }
    
    namespace PersistenceLayer {
        class Repository {
            <<Interface>>
            +save()
            +find()
            +update()
            +delete()
        }
        class DatabaseAccess {
            +execute_query()
            +manage_transactions()
        }
    }
    
    APIServices --> Facade : Uses
    Controllers --> Facade : Uses
    Facade --> Models : Manages
    Models --> Repository : Persisted by
    Repository --> DatabaseAccess : Uses
```

## Key Benefits of This Architecture

### Separation of Concerns
- Each layer has a single, well-defined responsibility
- Changes in one layer don't ripple through others
- Easier to test and maintain

### Facade Pattern Advantages
- **Simplified Interface**: Single entry point for business logic
- **Decoupling**: Presentation layer doesn't know about persistence details
- **Flexibility**: Easy to swap implementations without affecting clients
- **Centralized Logic**: Business rules are consolidated in one place

### Scalability
- Layers can be scaled independently
- Easy to add new features without disrupting existing code
- Clear boundaries for team collaboration

## Communication Flow Example

1. **Client Request** → API Services (Presentation Layer)
2. **API Services** → Facade (Business Logic Layer)
3. **Facade** → Models (Business Logic Layer)
4. **Models** → Repository (Persistence Layer)
5. **Repository** → Database (Persistence Layer)
6. **Response flows back** through the same path

## Implementation Notes

- All inter-layer communication goes through well-defined interfaces
- The Facade acts as a gatekeeper, enforcing business rules before data operations
- Persistence layer is completely isolated from presentation concerns
- This architecture supports easy migration to microservices if needed

---

**Created by:** Norah Mohammed Alskran  
**Project:** HBnB Evolution - Part 1  
**Date:** December 2025
