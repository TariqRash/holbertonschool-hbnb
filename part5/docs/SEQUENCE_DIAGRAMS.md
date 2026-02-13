# HBnB V2 — Sequence Diagrams

## 1. OTP Authentication Flow

```
┌──────┐       ┌──────────┐       ┌──────────┐       ┌────────┐
│Client│       │  API     │       │  DB      │       │ Resend │
└──┬───┘       └────┬─────┘       └────┬─────┘       └───┬────┘
   │                │                   │                  │
   │ POST /auth/otp/request             │                  │
   │ { email }      │                   │                  │
   │───────────────►│                   │                  │
   │                │ Find/Create User  │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Generate OTP (6-digit, 10min)        │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Send OTP Email    │                  │
   │                │─────────────────────────────────────►│
   │                │                   │                  │
   │  { message: "OTP sent" }           │                  │
   │◄───────────────│                   │                  │
   │                │                   │                  │
   │ POST /auth/otp/verify              │                  │
   │ { email, code }│                   │                  │
   │───────────────►│                   │                  │
   │                │ Validate OTP      │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Mark OTP used     │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Generate JWT      │                  │
   │                │──────┐            │                  │
   │                │◄─────┘            │                  │
   │                │                   │                  │
   │  { access_token, refresh_token, user }                │
   │◄───────────────│                   │                  │
```

## 2. Magic Link Authentication Flow

```
┌──────┐       ┌──────────┐       ┌──────────┐       ┌────────┐
│Client│       │  API     │       │  DB      │       │ Resend │
└──┬───┘       └────┬─────┘       └────┬─────┘       └───┬────┘
   │                │                   │                  │
   │ POST /auth/magic-link/request      │                  │
   │ { email }      │                   │                  │
   │───────────────►│                   │                  │
   │                │ Find/Create User  │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Generate Token (UUID, 30min)         │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Send Magic Link Email                │
   │                │─────────────────────────────────────►│
   │  { message }   │                   │                  │
   │◄───────────────│                   │                  │
   │                │                   │                  │
   │ ─── User clicks link in email ─── │                  │
   │                │                   │                  │
   │ GET /auth/verify?token=abc123      │                  │
   │───────────────►│                   │                  │
   │                │ Validate Token    │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Mark Token used   │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │  { access_token, refresh_token, user }                │
   │◄───────────────│                   │                  │
```

## 3. Booking + Payment Flow

```
┌──────┐       ┌──────────┐       ┌──────────┐       ┌────────┐
│Guest │       │  API     │       │  DB      │       │ Stripe │
└──┬───┘       └────┬─────┘       └────┬─────┘       └───┬────┘
   │                │                   │                  │
   │ POST /bookings/check-availability  │                  │
   │ { place_id, check_in, check_out }  │                  │
   │───────────────►│                   │                  │
   │                │ Check conflicts   │                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │  { available: true, total_price }  │                  │
   │◄───────────────│                   │                  │
   │                │                   │                  │
   │ POST /bookings │                   │                  │
   │ { place_id, dates, guests }        │                  │
   │───────────────►│                   │                  │
   │                │ Calculate price   │                  │
   │                │──────┐            │                  │
   │                │◄─────┘            │                  │
   │                │ Create Booking    │                  │
   │                │  (status: pending)│                  │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │  { booking_id, total_price }       │                  │
   │◄───────────────│                   │                  │
   │                │                   │                  │
   │ POST /payments/create-intent       │                  │
   │ { booking_id } │                   │                  │
   │───────────────►│                   │                  │
   │                │ Create PaymentIntent                 │
   │                │─────────────────────────────────────►│
   │                │                   │                  │
   │                │ Store payment record                 │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │  { client_secret }                 │                  │
   │◄───────────────│                   │                  │
   │                │                   │                  │
   │ ── Client-side Stripe payment ──   │                  │
   │                │                   │                  │
   │                │ Webhook: payment_intent.succeeded     │
   │                │◄─────────────────────────────────────│
   │                │                   │                  │
   │                │ Update booking → confirmed            │
   │                │──────────────────►│                  │
   │                │                   │                  │
   │                │ Send confirmation email               │
   │                │─────────────────────────────────────►│
```

## 4. Place Search with Privacy

```
┌──────┐       ┌──────────┐       ┌──────────┐
│Client│       │  API     │       │  DB      │
└──┬───┘       └────┬─────┘       └────┬─────┘
   │                │                   │
   │ GET /places?city_id=X&type=Y       │
   │───────────────►│                   │
   │                │ Query with filters│
   │                │──────────────────►│
   │                │                   │
   │                │ Apply privacy:    │
   │                │ - Hide exact lat/lng
   │                │ - Hide address    │
   │                │ - Hide access info│
   │                │──────┐            │
   │                │◄─────┘            │
   │                │                   │
   │  [{ title, city, price, approx_location }]
   │◄───────────────│                   │
   │                │                   │
   │ GET /maps/places                   │
   │───────────────►│                   │
   │                │ Return markers    │
   │                │ with ±500mi offset│
   │                │──────────────────►│
   │                │                   │
   │  [{ lat (approx), lng (approx), title, price }]
   │◄───────────────│                   │
```

## 5. Post-Booking Access Reveal

```
┌──────┐       ┌──────────┐       ┌──────────┐
│Guest │       │  API     │       │  DB      │
└──┬───┘       └────┬─────┘       └────┬─────┘
   │                │                   │
   │ GET /bookings/123                  │
   │ (status: confirmed)                │
   │───────────────►│                   │
   │                │ Check booking     │
   │                │ status = confirmed│
   │                │──────────────────►│
   │                │                   │
   │                │ Include:          │
   │                │ - Exact address   │
   │                │ - Floor number    │
   │                │ - Door description│
   │                │ - Access code     │
   │                │ - Check-in time   │
   │                │──────┐            │
   │                │◄─────┘            │
   │                │                   │
   │  { ...booking, access_instructions, address }
   │◄───────────────│                   │
   │                │                   │
   │ GET /maps/place/456/exact          │
   │───────────────►│                   │
   │                │ Verify booking    │
   │                │──────────────────►│
   │                │                   │
   │  { exact_lat, exact_lng }          │
   │◄───────────────│                   │
```

## 6. Owner Registration Flow

```
┌──────┐       ┌──────────┐       ┌──────────┐
│Owner │       │  API     │       │  DB      │
└──┬───┘       └────┬─────┘       └────┬─────┘
   │                │                   │
   │ POST /auth/register/owner          │
   │ { name, email, password, phone }   │
   │───────────────►│                   │
   │                │ Check email unique │
   │                │──────────────────►│
   │                │                   │
   │                │ Create User       │
   │                │ (role: owner)     │
   │                │──────────────────►│
   │                │                   │
   │                │ Generate JWT      │
   │                │──────┐            │
   │                │◄─────┘            │
   │                │                   │
   │  { access_token, user }            │
   │◄───────────────│                   │
   │                │                   │
   │ POST /places   │                   │
   │ { property details }               │
   │───────────────►│                   │
   │                │ Create Place      │
   │                │──────────────────►│
   │                │                   │
   │  { place_id }  │                   │
   │◄───────────────│                   │
```
