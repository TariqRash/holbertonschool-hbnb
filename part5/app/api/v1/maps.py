"""
HBnB V2 — Maps API
Geocoding and map helpers. Uses Leaflet (free) by default.
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.place import Place
from app.models.booking import Booking
import math


@api_v1.route('/maps/places', methods=['GET'])
def map_places():
    """Get place markers for map — with privacy radius"""
    lang = request.args.get('lang', 'ar')
    city_id = request.args.get('city_id')

    query = Place.query.filter_by(is_active=True)
    if city_id:
        query = query.filter_by(city_id=city_id)

    places = query.all()

    markers = []
    for place in places:
        markers.append({
            'id': place.id,
            'title': place.title_ar if lang == 'ar' else place.title_en,
            'latitude': round(place.latitude, 1),  # ~11km precision (privacy)
            'longitude': round(place.longitude, 1),
            'price': place.price_per_night,
            'currency': place.currency,
            'rating': place.average_rating,
            'privacy_radius': current_app.config.get('PRIVACY_RADIUS_MILES', 500),
        })

    return jsonify({'markers': markers}), 200


@api_v1.route('/maps/place/<place_id>/exact', methods=['GET'])
@jwt_required()
def exact_location(place_id):
    """Get exact location — only for confirmed bookings"""
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)

    # Check if user has a confirmed booking
    booking = Booking.query.filter_by(
        place_id=place_id, guest_id=user_id,
    ).filter(Booking.status.in_(['confirmed', 'checked_in'])).first()

    if not booking and place.owner_id != user_id:
        return jsonify({
            'error': 'Book this place to see exact location',
            'error_ar': 'احجز هذا العقار لمشاهدة الموقع الدقيق'
        }), 403

    return jsonify({
        'latitude': place.latitude,
        'longitude': place.longitude,
        'address': place.address,
        'access_instructions': place.access_instructions_ar,
        'floor': place.floor_number,
        'door': place.door_description_ar,
    }), 200


@api_v1.route('/maps/nearby', methods=['GET'])
def nearby_places():
    """Find places near a coordinate"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius_km = request.args.get('radius', 50, type=float)
    lang = request.args.get('lang', 'ar')

    if not lat or not lng:
        return jsonify({'error': 'lat and lng required'}), 400

    # Simple distance filter (Haversine approximation)
    lat_range = radius_km / 111.0
    lng_range = radius_km / (111.0 * math.cos(math.radians(lat)))

    places = Place.query.filter(
        Place.is_active == True,
        Place.latitude.between(lat - lat_range, lat + lat_range),
        Place.longitude.between(lng - lng_range, lng + lng_range),
    ).all()

    return jsonify({
        'places': [p.to_card_dict(lang) for p in places],
        'center': {'lat': lat, 'lng': lng},
        'radius_km': radius_km,
    }), 200
