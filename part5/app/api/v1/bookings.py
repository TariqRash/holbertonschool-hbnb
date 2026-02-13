"""
HBnB V2 — Booking API
Full booking flow: check availability → create → pay → confirm.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.booking import Booking
from app.models.place import Place
from app.models.user import User
from datetime import datetime, date


# ─── Check Availability ─────────────────────────────────────
@api_v1.route('/bookings/check-availability', methods=['POST'])
def check_availability():
    """Check if a place is available for given dates"""
    data = request.get_json()
    place_id = data.get('place_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    if not all([place_id, check_in, check_out]):
        return jsonify({'error': 'place_id, check_in, check_out required'}), 400

    try:
        check_in_date = date.fromisoformat(check_in)
        check_out_date = date.fromisoformat(check_out)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if check_in_date >= check_out_date:
        return jsonify({'error': 'check_out must be after check_in'}), 400

    if check_in_date < date.today():
        return jsonify({'error': 'Cannot book in the past'}), 400

    place = Place.query.get_or_404(place_id)

    # Check for overlapping confirmed bookings
    conflict = Booking.query.filter(
        Booking.place_id == place_id,
        Booking.status.in_(['confirmed', 'checked_in']),
        Booking.check_in < check_out_date,
        Booking.check_out > check_in_date,
    ).first()

    nights = (check_out_date - check_in_date).days
    subtotal = place.price_per_night * nights
    discount = 0
    booking_type = 'nightly'

    if nights >= 30:
        booking_type = 'monthly'
        discount = subtotal * (place.monthly_discount / 100)

    service_fee = round((subtotal - discount) * 0.05, 2)
    total = round(subtotal - discount + service_fee, 2)

    return jsonify({
        'available': conflict is None,
        'place_id': place_id,
        'check_in': check_in,
        'check_out': check_out,
        'nights': nights,
        'price_per_night': place.price_per_night,
        'subtotal': subtotal,
        'discount': round(discount, 2),
        'service_fee': service_fee,
        'total': total,
        'booking_type': booking_type,
        'currency': place.currency,
    }), 200


# ─── Create Booking ─────────────────────────────────────────
@api_v1.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    user_id = get_jwt_identity()
    data = request.get_json()

    place_id = data.get('place_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    if not all([place_id, check_in, check_out]):
        return jsonify({'error': 'place_id, check_in, check_out required'}), 400

    place = Place.query.get_or_404(place_id)

    # Owners can't book their own
    if place.owner_id == user_id:
        return jsonify({
            'error': 'Cannot book your own property',
            'error_ar': 'لا يمكنك حجز عقارك الخاص'
        }), 400

    try:
        check_in_date = date.fromisoformat(check_in)
        check_out_date = date.fromisoformat(check_out)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Check availability
    conflict = Booking.query.filter(
        Booking.place_id == place_id,
        Booking.status.in_(['confirmed', 'checked_in']),
        Booking.check_in < check_out_date,
        Booking.check_out > check_in_date,
    ).first()

    if conflict:
        return jsonify({
            'error': 'Place not available for these dates',
            'error_ar': 'العقار غير متاح في هذه التواريخ'
        }), 409

    # Check guest count
    total_guests = data.get('adults', 1) + data.get('children', 0)
    if total_guests > place.max_guests:
        return jsonify({
            'error': f'Max {place.max_guests} guests allowed',
            'error_ar': f'الحد الأقصى {place.max_guests} ضيوف'
        }), 400

    booking = Booking(
        place_id=place_id,
        guest_id=user_id,
        check_in=check_in_date,
        check_out=check_out_date,
        adults=data.get('adults', 1),
        children=data.get('children', 0),
        infants=data.get('infants', 0),
        special_requests=data.get('special_requests'),
    )
    booking.calculate_price(place)

    db.session.add(booking)
    db.session.commit()

    lang = request.args.get('lang', 'ar')
    return jsonify({
        'message': 'Booking created',
        'message_ar': 'تم إنشاء الحجز',
        'booking': booking.to_dict(lang)
    }), 201


# ─── Get My Bookings ────────────────────────────────────────
@api_v1.route('/bookings', methods=['GET'])
@jwt_required()
def my_bookings():
    """Get current user's bookings"""
    user_id = get_jwt_identity()
    lang = request.args.get('lang', 'ar')
    status = request.args.get('status')

    query = Booking.query.filter_by(guest_id=user_id)
    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(Booking.created_at.desc()).all()

    return jsonify({
        'bookings': [b.to_dict(lang, include_access=True) for b in bookings]
    }), 200


# ─── Get Booking Detail ─────────────────────────────────────
@api_v1.route('/bookings/<booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get booking details — with access info if confirmed"""
    user_id = get_jwt_identity()
    lang = request.args.get('lang', 'ar')
    booking = Booking.query.get_or_404(booking_id)

    if booking.guest_id != user_id:
        # Check if owner
        if not booking.place or booking.place.owner_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

    include_access = booking.status in ('confirmed', 'checked_in')
    return jsonify(booking.to_dict(lang, include_access=include_access)), 200


# ─── Cancel Booking ──────────────────────────────────────────
@api_v1.route('/bookings/<booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    user_id = get_jwt_identity()
    booking = Booking.query.get_or_404(booking_id)

    if booking.guest_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if booking.status not in ('pending', 'confirmed'):
        return jsonify({
            'error': 'Cannot cancel this booking',
            'error_ar': 'لا يمكن إلغاء هذا الحجز'
        }), 400

    booking.status = 'cancelled'
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_reason = request.get_json().get('reason', '')
    db.session.commit()

    return jsonify({
        'message': 'Booking cancelled',
        'message_ar': 'تم إلغاء الحجز'
    }), 200


# ─── Owner: Get Place Bookings ──────────────────────────────
@api_v1.route('/owner/bookings', methods=['GET'])
@jwt_required()
def owner_bookings():
    """Get all bookings for owner's properties"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    lang = request.args.get('lang', 'ar')

    if not user or not user.is_owner:
        return jsonify({'error': 'Owner access required'}), 403

    bookings = Booking.query.join(Place).filter(
        Place.owner_id == user_id
    ).order_by(Booking.created_at.desc()).all()

    return jsonify({
        'bookings': [b.to_dict(lang) for b in bookings]
    }), 200


# ─── Owner: Confirm Booking ─────────────────────────────────
@api_v1.route('/owner/bookings/<booking_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_booking(booking_id):
    """Owner confirms a booking"""
    user_id = get_jwt_identity()
    booking = Booking.query.get_or_404(booking_id)

    if not booking.place or booking.place.owner_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if booking.status != 'pending':
        return jsonify({'error': 'Booking not in pending state'}), 400

    booking.status = 'confirmed'
    db.session.commit()

    return jsonify({
        'message': 'Booking confirmed',
        'message_ar': 'تم تأكيد الحجز'
    }), 200
