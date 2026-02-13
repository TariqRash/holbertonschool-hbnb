# 🏠 HBnB V2 — Gatherin-Style Vacation Rental Platform

<div align="center">

**منصة حجز العقارات — HBnB V2**

A fully-featured vacation rental platform inspired by [Gatherin](https://gatherin.sa),
built with Flask, SQLAlchemy, and modern Arabic-first UI.

[العربية](#arabic) · [English](#english) · [API Docs](docs/API.md) · [Architecture](docs/ARCHITECTURE.md)

</div>

---

## 🌟 Features

### 🔐 Authentication
- **Magic Link Login** — Passwordless via email (Resend SDK)
- **OTP Login** — 6-digit code via email
- **Owner Registration** — Property owners create accounts easily
- **JWT Tokens** — Secure session management

### 🏘️ Property Management
- **Property Types** — شقق، شاليهات، استديوهات، استراحات، منتجعات، فلل، مزارع، مخيمات
- **Media Upload** — Multiple images per property
- **Amenity Icons** — Visual amenity indicators
- **Access Instructions** — Post-booking only (door, floor, appearance)
- **Privacy Radius** — 500-mile radius shown pre-booking; exact location post-booking

### 📍 Maps
- **Leaflet + OpenStreetMap** — Free, no API key required
- **Google Maps** — Optional premium integration
- **Privacy Circle** — Blurred location before booking
- **Directions** — Post-booking navigation

### 📅 Booking System
- **Date Selection** — Check-in/out calendar
- **Instant Booking** — Real-time availability
- **Monthly Residency** — 30-day stays with 10% discount
- **Guest Count** — Adults, children, infants

### 💳 Payment Gateway
- **Stripe Integration** — Credit/debit cards
- **Booking Confirmation** — Email receipt via Resend
- **Refund Policy** — Configurable cancellation windows

### 🌍 Localization
- **Arabic (العربية)** — Default language, RTL support
- **English** — Full translation
- **Auto-Translation** — Google Translate API fallback
- **Saudi Cities** — الرياض، جدة، مكة، المدينة، الدمام، أبها، الطائف، تبوك

### 🎨 Home Screen
1. **Search Bar** — With filters (city, dates, guests, type)
2. **City Cards** — Browse by Saudi city
3. **Elite Slider** — Featured premium properties
4. **Trip Type** — Business or Family
5. **Monthly Residency** — Discounted long stays
6. **Property Type Cards** — Browse by category
7. **Budget Section** — Properties below average daily price

---

## 👥 Team

| Name | Role |
|------|------|
| **Tariq Almutairi** | Lead Developer |
| **Shaden** | Backend Developer |
| **Nora** | Frontend Developer |

---

## 🚀 Quick Start

```bash
# Clone and switch to V2 branch
git clone https://github.com/TariqRash/holbertonschool-hbnb.git
cd holbertonschool-hbnb
git checkout hbnb-v2
cd part5

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup database
./setup_database.sh

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the app
python3 run.py
```

Open http://localhost:5000 🎉

---

## 📁 Project Structure

```
part5/
├── run.py                  # Application entry point
├── config.py               # Configuration (dev/prod)
├── requirements.txt        # Python dependencies
├── setup_database.sh       # Database initialization
├── .env.example            # Environment template
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py         # User + Owner model
│   │   ├── place.py        # Property model
│   │   ├── booking.py      # Booking model
│   │   ├── payment.py      # Payment model
│   │   ├── review.py       # Review model
│   │   ├── amenity.py      # Amenity with icons
│   │   ├── media.py        # Property images
│   │   ├── city.py         # Saudi cities
│   │   └── otp.py          # OTP/Magic Link tokens
│   ├── api/v1/             # REST API endpoints
│   │   ├── auth.py         # Login/Register/OTP/Magic Link
│   │   ├── places.py       # Property CRUD
│   │   ├── bookings.py     # Booking flow
│   │   ├── payments.py     # Payment processing
│   │   ├── reviews.py      # Review CRUD
│   │   ├── amenities.py    # Amenity CRUD
│   │   ├── media.py        # Image upload
│   │   ├── cities.py       # City listing
│   │   └── maps.py         # Map/geocoding
│   ├── services/           # Business logic
│   │   ├── facade.py       # Service facade
│   │   ├── email_service.py # Resend email
│   │   └── translation.py  # Google Translate
│   ├── persistence/        # Database layer
│   │   └── repository.py   # SQLAlchemy repository
│   ├── templates/          # Jinja2 email templates
│   └── static/             # Frontend assets
│       ├── css/
│       ├── js/
│       ├── images/
│       └── icons/
├── docs/                   # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── SEQUENCE_DIAGRAMS.md
└── tests/                  # Test suite
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | ✅ |
| `JWT_SECRET_KEY` | JWT signing key | ✅ |
| `RESEND_API_KEY` | Resend email API key | ✅ |
| `GOOGLE_MAPS_API_KEY` | Google Maps (optional) | ❌ |
| `STRIPE_SECRET_KEY` | Stripe payments | ✅ |
| `STRIPE_PUBLISHABLE_KEY` | Stripe frontend key | ✅ |
| `DATABASE_URL` | Database connection | ❌ (defaults SQLite) |

---

<div dir="rtl" id="arabic">

## 🇸🇦 نبذة عن المشروع

منصة **HBnB V2** هي منصة حجز عقارات مستوحاة من تطبيق **قذرن** السعودي.
تتيح للمستخدمين حجز الشقق والشاليهات والفلل والمزارع وغيرها بسهولة تامة.

### المميزات:
- 🔐 تسجيل دخول بدون كلمة مرور (رابط سحري أو رمز تحقق)
- 🏘️ أنواع عقارات متعددة
- 📍 خرائط تفاعلية
- 📅 نظام حجز متكامل
- 💳 بوابة دفع إلكتروني
- 🌍 دعم العربية والإنجليزية

</div>

---

**Built with ❤️ by Tariq, Shaden & Nora**
