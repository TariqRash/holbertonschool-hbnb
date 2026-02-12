# HBnB Simple Web Client - Part 4

A front-end web client for the HBnB (Holberton BnB) application built with **HTML5**, **CSS3**, and **vanilla JavaScript**. This client communicates with the Part 3 Flask REST API to provide a complete user experience for browsing places, viewing details, and submitting reviews.

## ✨ Features

### Core Functionality
- **Login** with JWT authentication (cookie-based)
- **Browse places** with price filtering
- **Place details** with amenities and reviews
- **Submit reviews** with star ratings (authenticated users)

### Enhanced Features
- 🌍 **Language Switcher** — English / Arabic (RTL support)
- 🌙 **Dark / Light Mode** — Theme toggle with localStorage persistence
- 🔔 **Toast Notifications** — Elegant toasts replacing browser alerts
- ✏️ **Lucide Icons** — Beautiful open-source SVG icons
- 🅰️ **Premium Typography** — Playfair Display headings + Inter body
- 📱 **Responsive Design** — Mobile-first with smooth page transitions
- 🛡️ **Admin Panel** — Full CRUD dashboard for managing all entities

## Pages

| Page | File | Description |
|------|------|-------------|
| **Index** | `index.html` | Displays all available places as cards with a price filter |
| **Login** | `login.html` | Authentication form with email/password |
| **Place Details** | `place.html` | Detailed view of a place with reviews and amenities |
| **Add Review** | `add_review.html` | Standalone review submission form (authenticated only) |
| **Admin Login** | `admin/login.html` | Admin-only login (checks `is_admin` JWT claim) |
| **Admin Dashboard** | `admin/index.html` | Stats overview with recent users and places |
| **Admin Users** | `admin/users.html` | User management with create/edit modal |
| **Admin Places** | `admin/places.html` | Place management with delete |
| **Admin Reviews** | `admin/reviews.html` | Review moderation with delete |
| **Admin Amenities** | `admin/amenities.html` | Amenity CRUD with modal |

## Project Structure

```
part4/
├── index.html              # Main page - list of places with price filter
├── login.html              # Login form page
├── place.html              # Place details with reviews
├── add_review.html         # Review submission form
├── styles.css              # All CSS styles (responsive, dark mode, RTL)
├── scripts.js              # Main JavaScript logic (API calls, DOM, theme, i18n)
├── i18n.js                 # Internationalization - EN/AR translations
├── toast.js                # Toast notification system (JS)
├── toast.css               # Toast notification styles
├── README.md               # This file
├── images/
│   ├── logo.png            # HBnB application logo
│   ├── icon.png            # Favicon (32x32)
│   ├── icon_bath.png       # Bath amenity icon
│   ├── icon_bed.png        # Bed amenity icon
│   └── icon_wifi.png       # WiFi amenity icon
└── admin/
    ├── login.html          # Admin login page
    ├── index.html          # Admin dashboard
    ├── users.html          # User management
    ├── places.html         # Place management
    ├── reviews.html        # Review moderation
    ├── amenities.html      # Amenity CRUD
    ├── admin.js            # Admin panel JavaScript
    └── styles.css          # Admin panel dark theme
```

## Setup & Running

### Prerequisites

- Part 3 API server running (Flask backend)
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Any static file server (Python's `http.server`, VS Code Live Server, etc.)

### 1. Start the API Server (Part 3)

```bash
cd part3
pip install -r requirements.txt
python run.py
```

The API will be available at `http://127.0.0.1:5000/api/v1`

### 2. Serve the Frontend

```bash
cd part4
python3 -m http.server 8080
```

Then open `http://localhost:8080/index.html` in your browser.

### 3. Configuration

If your API runs on a different port, update the `API_BASE_URL` constant at the top of `scripts.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
```

> **Note:** Make sure CORS is enabled in the Part 3 API (`flask-cors` is configured in `part3/app/__init__.py`).

---

## Testing Guide

### Testing the Login Functionality (Task 2)

1. **Start both servers** (API on port 5000, frontend on port 8080).
2. **Navigate to** `http://localhost:8080/login.html`.
3. **Test with valid credentials**:
   - Enter email: `admin@hbnb.io` and password: `admin1234`
   - Click "Sign In"
   - **Expected**: User is redirected to `index.html`, the Login link in the header disappears
4. **Verify token storage**:
   - Open browser DevTools → Application → Cookies
   - A cookie named `token` should be present with the JWT value
5. **Test with invalid credentials**:
   - Enter a wrong email or password
   - Click "Sign In"
   - **Expected**: An error message appears below the form ("Login failed — please check your credentials")
6. **Test authentication persistence**:
   - After logging in, navigate to `index.html`
   - The "Login" link in the header should be hidden
   - Refresh the page — the login link should remain hidden (token persists in cookie)

### Testing the Places List & Filter (Task 3)

1. **Navigate to** `http://localhost:8080/index.html`.
2. **Expected**: All places load as cards showing title, price per night, description snippet, and a "View Details" button.
3. **Test the price filter**:
   - Select "Under $100" from the dropdown
   - **Expected**: Only places priced at $100 or below are shown
   - Select "All Prices"
   - **Expected**: All places reappear
4. **Test login link visibility**:
   - When not logged in: "Login" link should be visible in the header
   - When logged in: "Login" link should be hidden

### Testing Place Details (Task 4)

1. **Click "View Details"** on any place card from the index page.
2. **Expected**: The page shows:
   - Place title, price per night, host name
   - Full description
   - List of amenities as tags
   - Reviews section with reviewer name, star rating, and comment text
3. **Test add review access**:
   - When **not logged in**: The "Add a Review" form should be hidden
   - When **logged in**: The "Add a Review" form should be visible
4. **Test invalid place ID**:
   - Navigate to `place.html?id=invalid-uuid`
   - **Expected**: An error message is displayed ("Place not found")

### Testing the Add Review Functionality (Task 5)

1. **Log in first** using valid credentials on `login.html`.
2. **Navigate to a place details page** (`place.html?id=<valid-place-id>`).
3. **Submit a review using the inline form on place.html**:
   - Write a review in the text area
   - Select a rating (1-5 stars)
   - Click "Submit Review"
   - **Expected**: Success message appears, form clears
4. **Test the standalone add_review.html page**:
   - Navigate to `add_review.html?place_id=<valid-place-id>`
   - Submit a review
   - **Expected**: Success message, user is redirected to the place page
5. **Test without authentication**:
   - Clear cookies (DevTools → Application → Cookies → delete `token`)
   - Navigate to `add_review.html?place_id=<some-id>`
   - **Expected**: User is redirected to `index.html` (unauthenticated users cannot access the review form)
6. **Test validation**:
   - Try submitting with empty review text → form validation prevents submission
   - Try submitting without selecting a rating → error message: "Please select a rating"

---

## Key Implementation Details

### Authentication Flow
- JWT tokens are stored in browser cookies (`document.cookie`)
- The `getCookie('token')` helper reads the token on every page load
- Protected pages check for the token and redirect or hide elements accordingly
- The token is sent in the `Authorization: Bearer <token>` header for API requests

### Client-Side Price Filtering
- Places are fetched once from the API and stored in a global `allPlaces` array
- The price filter dropdown filters the stored array without making new API requests
- Filter options: All, Under $10, Under $50, Under $100

### XSS Protection
- All user-generated content is escaped via the `escapeHTML()` function before rendering into the DOM
- This prevents cross-site scripting attacks from review text or place descriptions

### Responsive Design
- Breakpoints at 768px (tablet) and 480px (mobile)
- CSS Grid layout for place cards adapts from 3 columns → 2 → 1
- Navigation collapses for smaller screens

### Dark / Light Mode
- Toggle via the moon/sun button in the header
- Saves preference to `localStorage` (`hbnb-theme`)
- Complete dark theme with adjusted CSS custom properties
- Header adopts a deep navy gradient in dark mode

### Language Switcher (i18n)
- Toggle between **English** and **Arabic** via the header button
- Arabic mode enables full RTL layout with `dir="rtl"` on `<html>`
- 50+ translated strings covering all UI text
- Saves preference to `localStorage` (`hbnb-lang`)
- Defaults to English so reviewers see English first

### Toast Notifications
- Beautiful slide-in notifications replace all `alert()` calls
- Four types: success (green), error (red), warning (amber), info (blue)
- Auto-dismiss with animated progress bar
- Click to dismiss, limited to 5 visible at once

### Admin Panel
- Accessible at `admin/login.html` (requires `is_admin: true` in JWT)
- **Dashboard**: Real-time stats cards (users, places, reviews, amenities)
- **Users**: View all users, create/edit via modal
- **Places**: View all places with owner info, delete functionality
- **Reviews**: Moderate reviews across all places, delete functionality
- **Amenities**: Full CRUD with create/edit modal and delete
- Dark professional theme with sidebar navigation
- Uses Lucide icons throughout
