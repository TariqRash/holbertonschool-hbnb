"""
HBnB V2 — Payment Model
Stripe payment integration.
"""
from app import db
from app.models.base_model import BaseModel


class Payment(BaseModel):
    """Payment model — Stripe integration"""
    __tablename__ = 'payments'

    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'), nullable=False, unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Stripe
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True, unique=True)
    stripe_customer_id = db.Column(db.String(255), nullable=True)

    # Amount
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='SAR')

    # Status: pending, processing, completed, failed, refunded
    status = db.Column(db.String(20), default='pending', index=True)

    # Payment method info
    payment_method = db.Column(db.String(50), nullable=True)  # card, apple_pay, etc.
    last_four = db.Column(db.String(4), nullable=True)
    brand = db.Column(db.String(20), nullable=True)  # visa, mastercard, mada

    # Refund
    refund_amount = db.Column(db.Float, nullable=True)
    refunded_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'last_four': self.last_four,
            'brand': self.brand,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
