# HBnB V2 — API Documentation

## Base URL
```
http://localhost:5001/api/v1
```

## Authentication

### Request OTP
```http
POST /auth/otp/request
Content-Type: application/json

{
    "email": "user@example.com"
}
```

### Verify OTP
```http
POST /auth/otp/verify
Content-Type: application/json

{
    "email": "user@example.com",
    "code": "123456"
}
```
**Response:**
```json
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": { "id": "...", "email": "...", "role": "guest" }
}
```

### Request Magic Link
```http
POST /auth/magic-link/request
Content-Type: application/json

{
    "email": "user@example.com"
}
```

### Verify Magic Link
```http
POST /auth/magic-link/verify
Content-Type: application/json

{
    "token": "abc123..."
}
```

### Password Login (Fallback)
```http
POST /auth/login
Content-Type: application/json

{
    "email": "admin@hbnb.sa",
    "password": "admin123"
}
```

### Register as Owner
```http
POST /auth/register/owner
Content-Type: application/json

{
    "first_name": "Mohammed",
    "last_name": "Ali",
    "email": "owner@example.com",
    "password": "securepass",
    "phone": "+966500000000"
}
```

### Get Profile
```http
GET /auth/me
Authorization: Bearer <token>
```

### Update Profile
```http
PUT /auth/me
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "Updated Name"
}
```

---

## Places

### List Places (with filters)
```http
GET /places?city_id=<id>&property_type_id=<id>&price_min=100&price_max=500&max_guests=4&trip_type=family&search=keyword&sort=price_asc&page=1&per_page=12&lang=ar
```

### Get Place Details
```http
GET /places/<place_id>?lang=ar
```
> **Privacy**: Before booking, coordinates are approximate (±500mi radius). After booking, exact location and access instructions are revealed.

### Featured Places
```http
GET /places/featured
```

### Trip Type Filter
```http
GET /places/trip/business
GET /places/trip/family
```

### Budget Friendly
```http
GET /places/budget
```

### Monthly Stays
```http
GET /places/monthly
```

### Home Page Data (aggregated)
```http
GET /home?lang=ar
```
Returns: `{ cities, featured, property_types, budget, monthly }`

### Create Place (Owner)
```http
POST /places
Authorization: Bearer <token>
Content-Type: application/json

{
    "title_ar": "...",
    "title_en": "...",
    "description_ar": "...",
    "description_en": "...",
    "price_per_night": 350,
    "city_id": "<id>",
    "property_type_id": "<id>",
    "bedrooms": 2,
    "bathrooms": 1,
    "max_guests": 4,
    "trip_type": "both"
}
```

### Property Types
```http
GET /property-types
```

---

## Bookings

### Check Availability
```http
POST /bookings/check-availability
Authorization: Bearer <token>
Content-Type: application/json

{
    "place_id": "<id>",
    "check_in": "2026-03-01",
    "check_out": "2026-03-05",
    "adults": 2
}
```

### Create Booking
```http
POST /bookings
Authorization: Bearer <token>
Content-Type: application/json

{
    "place_id": "<id>",
    "check_in": "2026-03-01",
    "check_out": "2026-03-05",
    "adults": 2,
    "children": 0,
    "special_requests": "Late check-in"
}
```

### My Bookings
```http
GET /bookings
Authorization: Bearer <token>
```

### Booking Details
```http
GET /bookings/<booking_id>
Authorization: Bearer <token>
```

### Cancel Booking
```http
POST /bookings/<booking_id>/cancel
Authorization: Bearer <token>
```

### Owner: View Bookings
```http
GET /owner/bookings
Authorization: Bearer <token>
```

### Owner: Confirm Booking
```http
POST /owner/bookings/<booking_id>/confirm
Authorization: Bearer <token>
```

---

## Payments

### Create Payment Intent
```http
POST /payments/create-intent
Authorization: Bearer <token>
Content-Type: application/json

{
    "booking_id": "<id>"
}
```
> **Demo Mode**: When `STRIPE_SECRET_KEY` is not configured, payments are simulated.

### Stripe Webhook
```http
POST /payments/webhook
```

---

## Reviews

### Get Place Reviews
```http
GET /places/<place_id>/reviews?page=1&per_page=10
```

### Submit Review (requires completed booking)
```http
POST /places/<place_id>/reviews
Authorization: Bearer <token>
Content-Type: application/json

{
    "booking_id": "<booking_id>",
    "rating": 5,
    "comment": "Great place!",
    "cleanliness": 5,
    "accuracy": 4,
    "location": 5,
    "value": 4,
    "communication": 5,
    "check_in": 5
}
```

---

## Cities

### List Cities
```http
GET /cities?featured=true
```

---

## Maps

### Get Map Markers (privacy-aware)
```http
GET /maps/places?city_id=<id>
```

### Get Exact Location (post-booking)
```http
GET /maps/place/<place_id>/exact
Authorization: Bearer <token>
```

### Nearby Places
```http
GET /maps/nearby?lat=24.7&lng=46.6&radius=10
```

---

## Amenities

### List Amenities
```http
GET /amenities?category=essentials
```

### Create Amenity (Admin)
```http
POST /amenities
Authorization: Bearer <token>
Content-Type: application/json

{
    "name_en": "Pool",
    "name_ar": "مسبح",
    "icon": "waves",
    "category": "leisure"
}
```

---

## Media

### Upload Property Image (Owner)
```http
POST /places/<place_id>/media
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <image file>
is_cover: true
caption_ar: "الواجهة الأمامية"
caption_en: "Front view"
```

---

## Test Accounts

| Role  | Email          | Password   |
|-------|---------------|------------|
| Admin | admin@hbnb.sa | admin123   |
| Owner | owner@hbnb.sa | owner123   |

---

## Error Responses
```json
{
    "error": "Error message in English or Arabic based on lang parameter"
}
```

## Status Codes
| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 409  | Conflict |
| 500  | Server Error |
