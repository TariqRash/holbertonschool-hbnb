"""
HBnB V2 — Payment API
Offline payment gateway: bank transfer, mada, cash on arrival.
"""
from datetime import datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.user import User


PAYMENT_METHODS = {
    'bank_transfer': {
        'name_en': 'Bank Transfer',
        'name_ar': 'تحويل بنكي',
        'icon': 'landmark',
        'instructions_ar': 'قم بالتحويل إلى الحساب المذكور أدناه وأرفق إيصال التحويل',
        'instructions_en': 'Transfer to the account below and upload the receipt',
    },
    'mada_transfer': {
        'name_en': 'Mada Transfer',
        'name_ar': 'تحويل مدى',
        'icon': 'credit-card',
        'instructions_ar': 'قم بالتحويل عبر مدى إلى الحساب المذكور أدناه',
        'instructions_en': 'Transfer via Mada to the account below',
    },
    'cash_on_arrival': {
        'name_en': 'Cash on Arrival',
        'name_ar': 'الدفع عند الوصول',
        'icon': 'banknote',
        'instructions_ar': 'ادفع نقداً عند الوصول إلى مكان الإقامة',
        'instructions_en': 'Pay cash when you arrive at the property',
    },
}


# ─── Payment Methods Info ────────────────────────────────────
@api_v1.route('/payments/methods', methods=['GET'])
def payment_methods():
    """List available payment methods with bank details"""
    bank_info = {
        'bank_name': current_app.config.get('BANK_NAME', 'الراجحي — Al Rajhi Bank'),
        'account_holder': current_app.config.get('ACCOUNT_HOLDER', 'Rizi Platform'),
        'iban': current_app.config.get('BANK_IBAN', 'SA03 8000 0000 6080 1016 7519'),
    }

    methods = []
    for key, info in PAYMENT_METHODS.items():
        m = {'id': key, **info}
        if key in ('bank_transfer', 'mada_transfer'):
            m['bank_info'] = bank_info
        methods.append(m)

    return jsonify(methods), 200


# ─── Create Payment ──────────────────────────────────────────
@api_v1.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    """Create an offline payment record for a booking"""
    user_id = get_jwt_identity()
    data = request.get_json()

    booking_id = data.get('booking_id')
    method = data.get('payment_method', 'bank_transfer')

    if not booking_id:
        return jsonify({'error': 'booking_id required'}), 400

    if method not in PAYMENT_METHODS:
        return jsonify({'error': f'Invalid method. Choose: {", ".join(PAYMENT_METHODS.keys())}'}), 400

    booking = Booking.query.get_or_404(booking_id)

    if booking.guest_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if booking.status not in ('pending',):
        return jsonify({'error': 'Booking already processed'}), 400

    # Check existing payment
    existing = Payment.query.filter_by(booking_id=booking_id).first()
    if existing and existing.status == 'completed':
        return jsonify({'error': 'Already paid'}), 400

    # Determine initial status
    if method == 'cash_on_arrival':
        status = 'awaiting_confirmation'
        booking.status = 'confirmed'
    else:
        status = 'awaiting_confirmation'

    payment = Payment(
        booking_id=booking_id,
        user_id=user_id,
        amount=booking.total_price,
        currency=booking.currency,
        payment_method=method,
        status=status,
        transfer_reference=data.get('transfer_reference'),
        bank_name=data.get('bank_name'),
        payment_notes=data.get('notes'),
    )

    if existing:
        db.session.delete(existing)

    db.session.add(payment)
    db.session.commit()

    method_info = PAYMENT_METHODS[method]
    return jsonify({
        'message': f'تم تسجيل الدفع عبر {method_info["name_ar"]}',
        'message_en': f'Payment registered via {method_info["name_en"]}',
        'payment': payment.to_dict(),
        'instructions_ar': method_info['instructions_ar'],
        'instructions_en': method_info['instructions_en'],
    }), 201


# ─── Upload Payment Receipt ─────────────────────────────────
@api_v1.route('/payments/<payment_id>/receipt', methods=['POST'])
@jwt_required()
def upload_receipt(payment_id):
    """Upload payment receipt (transfer confirmation)"""
    user_id = get_jwt_identity()
    payment = Payment.query.get_or_404(payment_id)

    if payment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    receipt_url = data.get('receipt_url')
    transfer_ref = data.get('transfer_reference')

    if receipt_url:
        payment.receipt_url = receipt_url
    if transfer_ref:
        payment.transfer_reference = transfer_ref

    payment.status = 'awaiting_confirmation'
    db.session.commit()

    return jsonify({
        'message': 'تم رفع الإيصال بنجاح',
        'message_en': 'Receipt uploaded successfully',
        'payment': payment.to_dict(),
    }), 200


# ─── Admin: Confirm Payment ─────────────────────────────────
@api_v1.route('/payments/<payment_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_payment(payment_id):
    """Admin confirms a payment (marks as completed)"""
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin or not admin.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    payment = Payment.query.get_or_404(payment_id)

    if payment.status == 'completed':
        return jsonify({'error': 'Already confirmed'}), 400

    payment.status = 'completed'
    payment.confirmed_by = admin_id
    payment.confirmed_at = datetime.utcnow()

    # Confirm the booking
    booking = Booking.query.get(payment.booking_id)
    if booking:
        booking.status = 'confirmed'

    db.session.commit()

    return jsonify({
        'message': 'تم تأكيد الدفع',
        'message_en': 'Payment confirmed',
        'payment': payment.to_dict(),
    }), 200


# ─── Admin: Reject Payment ──────────────────────────────────
@api_v1.route('/payments/<payment_id>/reject', methods=['POST'])
@jwt_required()
def reject_payment(payment_id):
    """Admin rejects a payment"""
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin or not admin.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json() or {}

    payment.status = 'failed'
    payment.payment_notes = data.get('reason', 'Payment rejected by admin')
    db.session.commit()

    return jsonify({
        'message': 'تم رفض الدفع',
        'message_en': 'Payment rejected',
        'payment': payment.to_dict(),
    }), 200


# ─── Admin: Pending Payments List ────────────────────────────
@api_v1.route('/payments/pending', methods=['GET'])
@jwt_required()
def pending_payments():
    """List all payments awaiting confirmation (admin)"""
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin or not admin.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    payments = Payment.query.filter_by(status='awaiting_confirmation').order_by(Payment.created_at.desc()).all()
    return jsonify([p.to_dict() for p in payments]), 200


# ─── Get Payment Status ─────────────────────────────────────
@api_v1.route('/payments/<payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    """Get payment details"""
    user_id = get_jwt_identity()
    payment = Payment.query.get_or_404(payment_id)

    user = User.query.get(user_id)
    if payment.user_id != user_id and not (user and user.is_admin):
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(payment.to_dict()), 200
