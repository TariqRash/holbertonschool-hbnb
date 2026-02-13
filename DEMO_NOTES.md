# Rizi — Demo Day Presentation Notes
## Holberton School HBnB Project

**Team:** Tariq Almutairi · Shaden Almansour · Norah Alsakran  
**Date:** February 16, 2026  
**Domain:** https://rizi.app  
**Repository:** https://github.com/TariqRash/holbertonschool-hbnb (branch: `hbnb-v2`)

---

## Opening Statement (30 seconds)

> "السلام عليكم — We're Team Rizi. We built a full-stack, production-ready vacation rental platform for the Saudi market. Arabic-first, bilingual, with a real booking engine, payment flow, admin panel, Google Maps, and passwordless authentication. Let us show you."

---

## What We Built — Feature Overview

### 1. Architecture & Tech Stack
- **Backend:** Python Flask with Blueprint architecture
- **Database:** SQLAlchemy ORM with Flask-Migrate (10 models, full relationships)
- **Authentication:** JWT (access + refresh tokens), passwordless OTP & magic link via Resend email API
- **Frontend:** Vanilla JS with no framework dependency — fast, lightweight, zero build step
- **Styling:** Custom CSS with design system — CSS variables, dark/light mode, RTL-first
- **Icons:** Lucide Icons (SVG-based, tree-shakable)
- **Maps:** Google Maps API integration for property locations
- **i18n:** Full Arabic/English bilingual support with real-time language switching

### 2. Database Models (10 Models)
| # | Model | Key Features |
|---|-------|-------------|
| 1 | **User** | Roles (admin/owner/guest), bcrypt hashing, email verification, avatar |
| 2 | **Place** | Bilingual titles, pricing, capacity, privacy radius for location |
| 3 | **PropertyType** | Categories (شقق، شاليهات، فلل، استراحات, etc.) with Lucide icons |
| 4 | **City** | Saudi cities with Arabic/English names and images |
| 5 | **Amenity** | Wi-Fi, pool, parking, etc. with Lucide icons and bilingual names |
| 6 | **Booking** | Full lifecycle (pending → confirmed → checked_in → completed → cancelled) |
| 7 | **Payment** | Stripe integration ready, payment tracking |
| 8 | **Review** | Rating (1-5), bilingual comments, verified guest reviews |
| 9 | **Media** | Multi-image support per property with ordering |
| 10 | **SiteSettings** | Admin-managed key-value config (API keys, booking rules) |

Plus: **OTP** model for email verification, **BaseModel** with UUID + timestamps.

### 3. API Endpoints (10 Route Files, 50+ Endpoints)
| Route File | Key Endpoints |
|-----------|--------------|
| `auth.py` | POST /register, POST /login, POST /verify-otp, GET /verify-magic-link, POST /refresh |
| `places.py` | GET /places (filtered, paginated), GET /places/featured, POST /places (owner), PUT /places/:id |
| `bookings.py` | POST /bookings/check-availability, POST /bookings, GET /bookings, POST /bookings/:id/cancel |
| `payments.py` | POST /payments/create-intent, POST /payments/confirm, GET /payments/:id |
| `reviews.py` | POST /reviews, GET /reviews, GET /reviews/place/:id |
| `amenities.py` | GET /amenities, POST /amenities (admin) |
| `cities.py` | GET /cities |
| `media.py` | POST /media/upload, DELETE /media/:id |
| `maps.py` | GET /maps/nearby, GET /maps/geocode |
| `users.py` | GET /users/me, PUT /users/me |
| `admin.py` | Full CRUD for all entities, GET /admin/dashboard, GET /config |

### 4. Frontend Pages (8 Templates)
| Page | File | What It Does |
|------|------|-------------|
| **Home** | `index.html` | Hero with search, property types, featured places, cities, trip types |
| **Search** | `search.html` | Filtered search with sidebar, map view, pagination |
| **Property Detail** | `place.html` | Gallery, amenities, reviews, booking sidebar, map |
| **Booking** | `booking.html` | Booking confirmation, payment, access instructions |
| **My Bookings** | `bookings.html` | Guest booking history with status tracking |
| **Owner Dashboard** | `owner.html` | Property management, booking management, analytics |
| **Login** | `login.html` | Email → OTP verification, passwordless |
| **Admin Panel** | `admin.html` | Full CRUD dashboard for all entities |

### 5. JavaScript Files (4 Files)
| File | Lines | Purpose |
|------|-------|---------|
| `config.js` | ~200 | API base URL, property type icons, toast notifications |
| `i18n.js` | ~150 | Arabic/English translations, RTL/LTR switching |
| `auth.js` | ~200 | JWT management, login/register flow, user state |
| `home.js` | ~260 | Home page data loading, rendering, search |
| `admin.js` | ~550 | Full admin panel CRUD operations |

### 6. CSS Design System (9 Stylesheets)
| File | Purpose |
|------|---------|
| `main.css` | Design tokens, navbar, cards, grids, footer, animations, responsive |
| `home.css` | Hero section, search box, filter chips |
| `login.css` | Login card, OTP inputs, ambient glow effects |
| `place.css` | Property detail gallery, booking sidebar, reviews, modals |
| `booking.css` | Booking confirmation layout, payment card, access info |
| `bookings.css` | Booking list, status badges |
| `search.css` | Search page layout, filters sidebar, map |
| `owner.css` | Owner dashboard layout |
| `admin.css` | Admin panel sidebar, tables, stats, modals |

---

## Key Technical Highlights (Talking Points)

### Privacy-Aware Location System
- Property locations are stored with exact coordinates
- **Before booking:** Users only see approximate location (~11km radius) — `round(latitude, 1)`
- **After confirmed booking:** Exact address, floor number, door description, and access instructions are revealed
- This protects property owners' privacy while still showing general area on the map

### Passwordless Authentication
- Users register with email only — no password to forget
- OTP (6-digit code) sent via Resend email API
- Magic link alternative for one-click login
- JWT access tokens (15 min) + refresh tokens (30 days)
- Automatic token refresh on expiry

### Bilingual Architecture
- Every user-facing string has Arabic and English versions
- Database stores both: `title_ar`, `title_en`, `description_ar`, `description_en`
- Frontend `i18n.js` handles real-time language switching
- RTL/LTR direction changes automatically
- Font switching: Cairo (Arabic) ↔ Inter (English)

### Booking Engine
- **Check-in time:** 4:00 PM (16:00)
- **Check-out time:** 12:00 PM (12:00)
- **Cleaning window:** 4 hours between guests
- **Pricing:** Nightly rate + 5% service fee
- **Monthly discount:** 10%+ discount for 30+ day stays
- **Overlap protection:** Database-level conflict checking

### Admin Panel
- Full CRUD for: Users, Places, Bookings, Reviews, Amenities, Cities, Property Types, Site Settings
- Dashboard with real-time stats (total users, places, bookings, revenue)
- API key management (Google Maps, Stripe)
- Booking rules configuration
- Role-based access control — only `is_admin` users can access

### Dark Mode
- System preference detection (`prefers-color-scheme`)
- Manual toggle with persistent localStorage
- All 9 CSS files support both themes via CSS custom properties
- Smooth transitions between themes

### UI/UX Design Details
- **Glass morphism navbar:** `backdrop-filter: blur(24px) saturate(180%)`
- **Spring animations:** `cubic-bezier(0.34, 1.56, 0.64, 1)` for bouncy interactions
- **Staggered card animations:** Cards fade in with cascade delays (0.05s increments)
- **Gradient buttons:** `linear-gradient(135deg)` with hover glow effect
- **Hero ambient orbs:** Floating gradient circles with `@keyframes floatOrb`
- **Heartbeat footer animation:** The ❤ icon pulses with CSS animation
- **Focus-visible accessibility:** Custom focus rings for keyboard navigation
- **Skeleton loading:** Shimmer effect while data loads

---

## Demo Flow Script (5 minutes)

### 1. Home Page (60 seconds)
- Show the hero section — dark gradient with floating orbs
- Point out the search box with city/date/guest filters
- Scroll down: Property types with Lucide icons
- Featured properties with card hover animations
- Cities section with overlay cards
- Trip types (business vs family)
- Footer with team names and Holberton credit

### 2. Dark Mode Toggle (15 seconds)
- Click theme toggle — instant switch
- Point out all elements adapt: navbar, cards, footer, everything

### 3. Language Switch (15 seconds)
- Switch to English — show RTL → LTR transition
- All content changes, layout mirrors

### 4. Search Page (45 seconds)
- Click on a city or type to navigate to search
- Show filters sidebar (price range, bedrooms, guests)
- Map view on the side
- Card grid with responsive layout

### 5. Login Flow (45 seconds)
- Click login — show the card with ambient glow effect
- Enter email → OTP sent
- Show OTP input with focus animations
- Authenticated → redirected to home

### 6. Property Detail (45 seconds)
- Click a property card
- Photo gallery grid
- Host info, amenities, reviews
- Booking sidebar with date picker and price calculation
- Map showing approximate location (privacy radius!)

### 7. Admin Panel (60 seconds)
- Navigate to `/admin`
- Dashboard with stats cards
- Users table — CRUD
- Places management
- Settings — API keys, booking rules
- Show sidebar navigation

### 8. Owner Dashboard (30 seconds)
- Show property listing management
- Booking requests and confirmation flow

---

## Questions We're Ready For

**Q: Why no password?**
A: Passwordless is more secure — no credentials to leak. OTP and magic links via email are the modern approach used by Notion, Slack, and others.

**Q: How do you handle location privacy?**
A: We store exact coordinates but expose only rounded values (1 decimal = ~11km) until the guest has a confirmed booking. Then we reveal the full address and access instructions.

**Q: Why vanilla JS instead of React/Vue?**
A: For this project scope, vanilla JS keeps the bundle at zero — no build step, instant loading. Our 4 JS files total ~900 lines. A React app would need 10x the infrastructure.

**Q: How does the admin panel work?**
A: JWT-based role checking. The `admin_required` decorator verifies `user.role == 'admin'`. Full REST API with CRUD operations for every entity. The frontend is a single-page admin panel with section navigation.

**Q: What about deployment?**
A: Config supports development, testing, and production environments. Production config includes secure cookie settings, HTTPS enforcement, and proper CORS. Database is SQLite for demo, but SQLAlchemy makes it trivial to switch to PostgreSQL.

**Q: How do you handle payments?**
A: Stripe integration is built in — create payment intent, confirm payment, webhook handling. Currently using test keys for the demo.

---

## File Count Summary

| Category | Files | Lines (approx) |
|----------|-------|----------------|
| Python Backend | 25 | ~3,500 |
| HTML Templates | 8 | ~2,200 |
| CSS Stylesheets | 9 | ~3,000 |
| JavaScript | 5 | ~1,400 |
| Config & Docs | 10 | ~800 |
| **Total** | **57** | **~10,900** |

---

## Team Contributions

### Tariq Almutairi
- Backend architecture (Flask, SQLAlchemy, JWT)
- API design and implementation
- Database modeling and migrations
- Admin panel (API + Frontend)
- Deployment configuration

### Shaden Almansour
- Frontend design and CSS
- Bilingual support (Arabic/English)
- UI/UX design system
- Template development
- Dark mode implementation

### Norah Alsakran
- Authentication system (OTP, magic links)
- Booking engine logic
- Email service integration
- Search and filter functionality
- Testing and quality assurance

---

## Closing Statement

> "We built Rizi from scratch — 57 files, nearly 11,000 lines of code, production-ready with a real admin panel, booking engine, and beautiful UI. Made with love for Holberton School. Thank you."

---

*This document is for presentation reference only — NOT committed to the repository.*
