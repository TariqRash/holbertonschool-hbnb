"""
HBnB V2 — Booking Model
Full booking lifecycle: pending → confirmed → checked_in → completed → reviewed
"""
from app import db
from app.models.base_model import BaseModel
from datetime import datetime, timezone


class Booking(BaseModel):
    """Booking model — reservation management"""
    __tablename__ = 'bookings'

    # References
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
    guest_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

    # Dates
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    # Guests
    adults = db.Column(db.Integer, default=1)
    children = db.Column(db.Integer, default=0)
    infants = db.Column(db.Integer, default=0)

    # Pricing
    price_per_night = db.Column(db.Float, nullable=False)
    total_nights = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    service_fee = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='SAR')

    # Status: pending, confirmed, cancelled, checked_in, completed
    status = db.Column(db.String(20), default='pending', index=True)
    booking_type = db.Column(db.String(20), default='nightly')  # nightly, monthly

    # Cancellation
    cancelled_at = db.Column(db.DateTime, nullable=True)
    cancellation_reason = db.Column(db.Text, nullable=True)

    # Special requests
    special_requests = db.Column(db.Text, nullable=True)

    # Payment
    payment = db.relationship('Payment', backref='booking', uselist=False)

    @property
    def is_active(self):
        return self.status in ('pending', 'confirmed', 'checked_in')

    @property
    def total_guests(self):
        return self.adults + self.children + self.infants

    @property
    def nights_count(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0

    def calculate_price(self, place):
        """Calculate total price with discounts"""
        nights = self.nights_count
        self.total_nights = nights
        self.price_per_night = place.price_per_night

        self.subtotal = place.price_per_night * nights

        # Monthly discount (30+ days)
        if nights >= 30:
            self.booking_type = 'monthly'
            self.discount_amount = self.subtotal * (place.monthly_discount / 100)
        else:
            self.discount_amount = 0

        # Service fee (5%)
        self.service_fee = round((self.subtotal - self.discount_amount) * 0.05, 2)

        self.total_price = round(self.subtotal - self.discount_amount + self.service_fee, 2)
        self.currency = place.currency

    def to_dict(self, lang='ar', include_access=False):
        data = {
            'id': self.id,
            'place_id': self.place_id,
            'guest_id': self.guest_id,
            'check_in': self.check_in.isoformat() if self.check_in else None,
            'check_out': self.check_out.isoformat() if self.check_out else None,
            'adults': self.adults,
            'children': self.children,
            'infants': self.infants,
            'total_guests': self.total_guests,
            'price_per_night': self.price_per_night,
            'total_nights': self.total_nights,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'service_fee': self.service_fee,
            'total_price': self.total_price,
            'currency': self.currency,
            'status': self.status,
            'booking_type': self.booking_type,
            'special_requests': self.special_requests,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        # Include place card data
        if self.place:
            if include_access and self.status in ('confirmed', 'checked_in'):
                data['place'] = self.place.to_dict(lang, include_private=True)
            else:
                data['place'] = self.place.to_card_dict(lang)

        return data
