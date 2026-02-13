"""
HBnB V2 — Payment Model
Offline payment methods: bank transfer, mada, cash on arrival.
"""
from app import db
from app.models.base_model import BaseModel


class Payment(BaseModel):
    """Payment model — offline payment methods"""
    __tablename__ = 'payments'

    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'), nullable=False, unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Amount
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='SAR')

    # Status: pending, awaiting_confirmation, completed, failed, refunded
    status = db.Column(db.String(20), default='pending', index=True)

    # Payment method: bank_transfer, mada_transfer, cash_on_arrival
    payment_method = db.Column(db.String(50), nullable=False, default='bank_transfer')

    # Offline payment details
    transfer_reference = db.Column(db.String(100), nullable=True)   # Bank transfer ref number
    bank_name = db.Column(db.String(100), nullable=True)            # Sender's bank name
    receipt_url = db.Column(db.String(500), nullable=True)          # Uploaded receipt image URL
    payment_notes = db.Column(db.Text, nullable=True)               # Additional notes from guest

    # Admin confirmation
    confirmed_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    # Refund
    refund_amount = db.Column(db.Float, nullable=True)
    refunded_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    confirmer = db.relationship('User', foreign_keys=[confirmed_by], lazy='select')

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'transfer_reference': self.transfer_reference,
            'bank_name': self.bank_name,
            'receipt_url': self.receipt_url,
            'payment_notes': self.payment_notes,
            'confirmed_by': self.confirmed_by,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
