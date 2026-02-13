"""
HBnB V2 — Payment API
Stripe payment integration for bookings.
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.payment import Payment
from app.models.booking import Booking


# ─── Create Payment Intent ──────────────────────────────────
@api_v1.route('/payments/create-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    """Create a Stripe payment intent for a booking"""
    user_id = get_jwt_identity()
    data = request.get_json()
    booking_id = data.get('booking_id')

    if not booking_id:
        return jsonify({'error': 'booking_id required'}), 400

    booking = Booking.query.get_or_404(booking_id)

    if booking.guest_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if booking.status != 'pending':
        return jsonify({'error': 'Booking already processed'}), 400

    # Check existing payment
    existing = Payment.query.filter_by(booking_id=booking_id).first()
    if existing and existing.status == 'completed':
        return jsonify({'error': 'Already paid'}), 400

    stripe_key = current_app.config.get('STRIPE_SECRET_KEY')

    if stripe_key:
        try:
            import stripe
            stripe.api_key = stripe_key

            # Convert SAR to halalas (smallest currency unit)
            amount_halalas = int(booking.total_price * 100)

            intent = stripe.PaymentIntent.create(
                amount=amount_halalas,
                currency=booking.currency.lower(),
                metadata={
                    'booking_id': booking_id,
                    'user_id': user_id,
                }
            )

            # Save payment record
            payment = Payment(
                booking_id=booking_id,
                user_id=user_id,
                amount=booking.total_price,
                currency=booking.currency,
                stripe_payment_intent_id=intent.id,
                status='processing',
            )
            db.session.add(payment)
            db.session.commit()

            return jsonify({
                'client_secret': intent.client_secret,
                'payment_id': payment.id,
                'publishable_key': current_app.config.get('STRIPE_PUBLISHABLE_KEY'),
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # Demo mode — auto-confirm without real payment
        payment = Payment(
            booking_id=booking_id,
            user_id=user_id,
            amount=booking.total_price,
            currency=booking.currency,
            status='completed',
            payment_method='demo',
        )
        booking.status = 'confirmed'
        db.session.add(payment)
        db.session.commit()

        return jsonify({
            'message': 'Payment completed (demo mode)',
            'message_ar': 'تم الدفع (وضع تجريبي)',
            'payment': payment.to_dict(),
            'demo': True,
        }), 200


# ─── Confirm Payment (Webhook) ──────────────────────────────
@api_v1.route('/payments/webhook', methods=['POST'])
def payment_webhook():
    """Stripe webhook for payment confirmation"""
    stripe_key = current_app.config.get('STRIPE_SECRET_KEY')

    if not stripe_key:
        return jsonify({'error': 'Stripe not configured'}), 400

    try:
        import stripe
        stripe.api_key = stripe_key

        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')

        event = stripe.Event.construct_from(
            stripe.util.json.loads(payload), stripe.api_key
        )

        if event.type == 'payment_intent.succeeded':
            intent = event.data.object
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=intent.id
            ).first()

            if payment:
                payment.status = 'completed'
                payment.payment_method = intent.payment_method_types[0] if intent.payment_method_types else 'card'

                # Confirm the booking
                booking = Booking.query.get(payment.booking_id)
                if booking:
                    booking.status = 'confirmed'

                db.session.commit()

        elif event.type == 'payment_intent.payment_failed':
            intent = event.data.object
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=intent.id
            ).first()
            if payment:
                payment.status = 'failed'
                db.session.commit()

        return jsonify({'received': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ─── Get Payment Status ─────────────────────────────────────
@api_v1.route('/payments/<payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    """Get payment details"""
    user_id = get_jwt_identity()
    payment = Payment.query.get_or_404(payment_id)

    if payment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(payment.to_dict()), 200
