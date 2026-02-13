# HBnB V2 — Architecture

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Jinja2)                 │
│  index.html │ login.html │ place.html │ booking.html│
│  search.html│ bookings.html │ owner.html            │
├─────────────────────────────────────────────────────┤
│                    Static Assets                     │
│  CSS: main.css, home.css, login.css, place.css ...  │
│  JS:  config.js, i18n.js, auth.js, home.js          │
├─────────────────────────────────────────────────────┤
│                   Flask App (API)                    │
│  Blueprint: api_v1 (/api/v1)                        │
│  Blueprint: frontend (/)                             │
├─────────────────────────────────────────────────────┤
│                    Services Layer                    │
│  EmailService (Resend) │ TranslationService          │
├─────────────────────────────────────────────────────┤
│                    Models (SQLAlchemy)               │
│  User, City, Place, PropertyType, Amenity, Booking  │
│  Payment, Review, Media, OTP                         │
├─────────────────────────────────────────────────────┤
│                    Database (SQLite/PostgreSQL)      │
└─────────────────────────────────────────────────────┘
│          External Services                           │
│  Resend (Email) │ Stripe (Payments) │ Leaflet (Maps)│
└──────────────────────────────────────────────────────┘
```

## Directory Structure

```
part5/
├── run.py                  # Entry point
├── config.py               # Configuration classes
├── seed.py                 # Database seeder
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── app/
│   ├── __init__.py         # App factory
│   ├── routes.py           # Frontend routes
│   ├── models/
│   │   ├── base_model.py   # Abstract base (UUID, timestamps)
│   │   ├── user.py         # User with roles & auth
│   │   ├── city.py         # Saudi cities
│   │   ├── place.py        # Properties + PropertyType
│   │   ├── amenity.py      # Amenity with icons
│   │   ├── booking.py      # Booking lifecycle
│   │   ├── payment.py      # Stripe payments
│   │   ├── review.py       # Reviews with sub-ratings
│   │   ├── media.py        # Property images
│   │   └── otp.py          # OTP & Magic Link tokens
│   ├── api/v1/
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── places.py       # Place CRUD + search
│   │   ├── bookings.py     # Booking management
│   │   ├── payments.py     # Payment processing
│   │   ├── reviews.py      # Review system
│   │   ├── amenities.py    # Amenity management
│   │   ├── media.py        # Image uploads
│   │   ├── cities.py       # City listing
│   │   ├── maps.py         # Map with privacy
│   │   └── users.py        # User profiles
│   ├── services/
│   │   ├── email_service.py    # Resend SDK integration
│   │   └── translation.py     # AR/EN translations
│   ├── templates/              # Jinja2 HTML
│   └── static/
│       ├── css/                # Stylesheets
│       └── js/                 # JavaScript modules
├── docs/
│   ├── API.md              # API documentation
│   ├── ARCHITECTURE.md     # This file
│   └── SEQUENCE_DIAGRAMS.md
└── tests/
```

## Key Design Patterns

### 1. App Factory Pattern
Flask app is created via `create_app()` allowing different configs (dev, prod, test).

### 2. Blueprint Architecture
- **api_v1**: RESTful JSON API at `/api/v1/*`
- **frontend**: Server-rendered pages at `/*`

### 3. Privacy-First Location
- Pre-booking: Approximate coordinates within 500-mile radius
- Post-booking: Exact location + access instructions revealed

### 4. Bilingual (AR/EN)
- All models have `_ar` and `_en` fields
- Frontend uses `data-t` attributes + `i18n.js` for live switching
- RTL/LTR auto-switches with language

### 5. Authentication Flow
```
Email → OTP/Magic Link → JWT Access + Refresh Tokens
```
- OTP: 6-digit code, 10min expiry, max 3 attempts
- Magic Link: Unique token, 30min expiry, one-time use
- Password: Optional fallback for admin/owner accounts

### 6. Booking Lifecycle
```
Guest Searches → Selects Place → Check Availability
→ Create Booking (pending) → Pay (Stripe)
→ Confirmed → Check-in → Completed
```

### 7. Payment Strategy
- **Production**: Real Stripe Payment Intents
- **Development**: Demo mode (auto-confirms without real charges)

## Database Models (ER)

```
User (1) ─────── (N) Place
  │                    │
  │                    ├── (N) Booking
  │                    ├── (N) Review
  │                    ├── (N) Media
  │                    └── (N↔N) Amenity
  │
  ├── (N) Booking ──── (1) Payment
  └── (N) Review

City (1) ──── (N) Place
PropertyType (1) ──── (N) Place
OTP (standalone - email-based)
```

## External Integrations

| Service | Purpose | SDK | Fallback |
|---------|---------|-----|----------|
| Resend | OTP & booking emails | `resend` Python SDK | Console log |
| Stripe | Payment processing | `stripe` Python SDK | Demo mode |
| Leaflet | Interactive maps | CDN (JS) | Static image |
| Google Translate | Auto-translate | `googletrans` | Manual dict |
| Lucide | Icon system | CDN (JS) | Emoji |

## Security

- JWT tokens with httpOnly cookies
- Bcrypt password hashing
- CORS configured per environment
- File upload validation (type + size)
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via Jinja2 auto-escaping
- Rate limiting on OTP requests
