"""
HBnB V2 — Reviews API
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.review import Review
from app.models.booking import Booking
from app.models.place import Place


@api_v1.route('/places/<place_id>/reviews', methods=['GET'])
def place_reviews(place_id):
    """Get reviews for a place"""
    lang = request.args.get('lang', 'ar')
    page = request.args.get('page', 1, type=int)

    Place.query.get_or_404(place_id)
    pagination = Review.query.filter_by(place_id=place_id, is_approved=True) \
        .order_by(Review.created_at.desc()) \
        .paginate(page=page, per_page=10, error_out=False)

    return jsonify({
        'reviews': [r.to_dict(lang) for r in pagination.items],
        'total': pagination.total,
    }), 200


@api_v1.route('/places/<place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    """Create a review — must have a completed booking, cannot be the owner"""
    user_id = get_jwt_identity()

    # Owner cannot review their own property
    place = Place.query.get_or_404(place_id)
    if place.owner_id == user_id:
        return jsonify({
            'error': 'Cannot review your own property',
            'error_ar': 'لا يمكنك تقييم عقارك الخاص'
        }), 403

    # Check if user has a completed booking
    booking = Booking.query.filter_by(
        place_id=place_id, guest_id=user_id,
    ).filter(Booking.status.in_(['completed', 'checked_in', 'confirmed'])).first()

    if not booking:
        return jsonify({
            'error': 'You must book this place before reviewing',
            'error_ar': 'يجب حجز هذا العقار قبل التقييم'
        }), 403

    # Check duplicate
    existing = Review.query.filter_by(place_id=place_id, user_id=user_id).first()
    if existing:
        return jsonify({
            'error': 'You already reviewed this place',
            'error_ar': 'لقد قمت بتقييم هذا العقار مسبقاً'
        }), 409

    data = request.get_json()
    rating = data.get('rating')

    if not rating or not (1 <= rating <= 5):
        return jsonify({'error': 'Rating 1-5 required'}), 400

    review = Review(
        place_id=place_id,
        user_id=user_id,
        booking_id=booking.id,
        rating=rating,
        cleanliness=data.get('cleanliness'),
        accuracy=data.get('accuracy'),
        location_rating=data.get('location_rating'),
        value=data.get('value'),
        communication=data.get('communication'),
        check_in_rating=data.get('check_in_rating'),
        comment=data.get('comment'),
        language=data.get('language', 'ar'),
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        'message': 'Review created',
        'message_ar': 'تم إضافة التقييم',
        'review': review.to_dict()
    }), 201


@api_v1.route('/places/<place_id>/user-status', methods=['GET'])
@jwt_required()
def place_user_status(place_id):
    """Check if the current user has booked / reviewed this place"""
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)

    is_owner = (place.owner_id == user_id)

    # Has a qualifying booking (completed, checked_in, or confirmed)?
    booking = Booking.query.filter_by(
        place_id=place_id, guest_id=user_id,
    ).filter(Booking.status.in_(['completed', 'checked_in', 'confirmed'])).first()

    has_booked = booking is not None

    # Already left a review?
    has_reviewed = Review.query.filter_by(
        place_id=place_id, user_id=user_id
    ).first() is not None

    return jsonify({
        'is_owner': is_owner,
        'has_booked': has_booked,
        'has_reviewed': has_reviewed,
        'can_review': has_booked and not has_reviewed and not is_owner,
    }), 200
