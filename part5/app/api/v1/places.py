"""
HBnB V2 — Places API
CRUD + search, filter, featured, by type, by city.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.api.v1 import api_v1
from app import db
from app.models.place import Place, PropertyType
from app.models.city import City
from app.models.amenity import Amenity
from app.models.booking import Booking
from app.models.user import User
from sqlalchemy import func


# ─── List Places (with filters) ─────────────────────────────
@api_v1.route('/places', methods=['GET'])
def list_places():
    """List properties with filtering and sorting"""
    lang = request.args.get('lang', 'ar')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Place.query.filter_by(is_active=True)

    # Filters
    city_id = request.args.get('city_id')
    if city_id:
        query = query.filter_by(city_id=city_id)

    property_type_id = request.args.get('property_type_id')
    if property_type_id:
        query = query.filter_by(property_type_id=property_type_id)

    trip_type = request.args.get('trip_type')
    if trip_type and trip_type in ('business', 'family'):
        query = query.filter(Place.trip_type.in_([trip_type, 'both']))

    min_price = request.args.get('min_price', type=float)
    if min_price is not None:
        query = query.filter(Place.price_per_night >= min_price)

    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        query = query.filter(Place.price_per_night <= max_price)

    max_guests = request.args.get('guests', type=int)
    if max_guests:
        query = query.filter(Place.max_guests >= max_guests)

    bedrooms = request.args.get('bedrooms', type=int)
    if bedrooms:
        query = query.filter(Place.bedrooms >= bedrooms)

    # Search
    search = request.args.get('q', '').strip()
    if search:
        query = query.filter(
            db.or_(
                Place.title_ar.ilike(f'%{search}%'),
                Place.title_en.ilike(f'%{search}%'),
                Place.description_ar.ilike(f'%{search}%'),
                Place.description_en.ilike(f'%{search}%'),
            )
        )

    # Sort
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        query = query.order_by(Place.price_per_night.asc())
    elif sort == 'price_high':
        query = query.order_by(Place.price_per_night.desc())
    elif sort == 'rating':
        query = query.order_by(Place.is_featured.desc())  # Simplified
    else:
        query = query.order_by(Place.created_at.desc())

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'places': [p.to_card_dict(lang) for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
    }), 200


# ─── Get Featured Places ────────────────────────────────────
@api_v1.route('/places/featured', methods=['GET'])
def featured_places():
    """Get elite/featured properties"""
    lang = request.args.get('lang', 'ar')
    limit = request.args.get('limit', 10, type=int)

    places = Place.query.filter_by(is_active=True, is_featured=True) \
        .order_by(Place.created_at.desc()).limit(limit).all()

    return jsonify({
        'places': [p.to_card_dict(lang) for p in places]
    }), 200


# ─── Get Places by Trip Type ────────────────────────────────
@api_v1.route('/places/trip/<trip_type>', methods=['GET'])
def places_by_trip_type(trip_type):
    """Get places by trip type: business or family"""
    lang = request.args.get('lang', 'ar')
    limit = request.args.get('limit', 10, type=int)

    if trip_type not in ('business', 'family'):
        return jsonify({'error': 'Invalid trip type'}), 400

    places = Place.query.filter_by(is_active=True) \
        .filter(Place.trip_type.in_([trip_type, 'both'])) \
        .limit(limit).all()

    return jsonify({
        'places': [p.to_card_dict(lang) for p in places],
        'trip_type': trip_type
    }), 200


# ─── Budget Places (below average price) ────────────────────
@api_v1.route('/places/budget', methods=['GET'])
def budget_places():
    """Get places below average daily price"""
    lang = request.args.get('lang', 'ar')
    limit = request.args.get('limit', 10, type=int)

    avg_price = db.session.query(func.avg(Place.price_per_night)) \
        .filter(Place.is_active == True).scalar() or 0

    places = Place.query.filter(
        Place.is_active == True,
        Place.price_per_night < avg_price
    ).order_by(Place.price_per_night.asc()).limit(limit).all()

    return jsonify({
        'places': [p.to_card_dict(lang) for p in places],
        'average_price': round(avg_price, 2),
        'currency': 'SAR'
    }), 200


# ─── Monthly Stay Deals ─────────────────────────────────────
@api_v1.route('/places/monthly', methods=['GET'])
def monthly_places():
    """Get places with monthly discount"""
    lang = request.args.get('lang', 'ar')
    limit = request.args.get('limit', 10, type=int)

    places = Place.query.filter(
        Place.is_active == True,
        Place.monthly_discount > 0
    ).order_by(Place.monthly_discount.desc()).limit(limit).all()

    return jsonify({
        'places': [p.to_card_dict(lang) for p in places]
    }), 200


# ─── Get Single Place ───────────────────────────────────────
@api_v1.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Get place details — privacy-aware"""
    lang = request.args.get('lang', 'ar')
    place = Place.query.get_or_404(place_id)

    # Check if user has an active booking
    include_private = False
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        try:
            from flask_jwt_extended import decode_token
            token_data = decode_token(auth_header.split(' ')[1])
            user_id = token_data.get('sub')
            booking = Booking.query.filter_by(
                place_id=place_id, guest_id=user_id,
            ).filter(Booking.status.in_(['confirmed', 'checked_in'])).first()
            if booking:
                include_private = True
            # Owners and admins can always see
            user = User.query.get(user_id)
            if user and (user.id == place.owner_id or user.is_admin):
                include_private = True
        except Exception:
            pass

    return jsonify(place.to_dict(lang, include_private=include_private)), 200


# ─── Create Place (Owner only) ──────────────────────────────
@api_v1.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new property listing"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_owner:
        return jsonify({
            'error': 'Only owners can create listings',
            'error_ar': 'فقط الملاك يمكنهم إضافة عقارات'
        }), 403

    data = request.get_json()
    required = ['title_ar', 'title_en', 'price_per_night', 'city_id',
                 'property_type_id', 'latitude', 'longitude']

    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    place = Place(
        title_en=data['title_en'],
        title_ar=data['title_ar'],
        description_en=data.get('description_en', ''),
        description_ar=data.get('description_ar', ''),
        price_per_night=data['price_per_night'],
        city_id=data['city_id'],
        property_type_id=data['property_type_id'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        owner_id=user_id,
        max_guests=data.get('max_guests', 4),
        bedrooms=data.get('bedrooms', 1),
        bathrooms=data.get('bathrooms', 1),
        beds=data.get('beds', 1),
        trip_type=data.get('trip_type', 'both'),
        address=data.get('address'),
        access_instructions_en=data.get('access_instructions_en'),
        access_instructions_ar=data.get('access_instructions_ar'),
        floor_number=data.get('floor_number'),
        door_description_en=data.get('door_description_en'),
        door_description_ar=data.get('door_description_ar'),
        check_in_time=data.get('check_in_time', '15:00'),
        check_out_time=data.get('check_out_time', '11:00'),
        rules_en=data.get('rules_en'),
        rules_ar=data.get('rules_ar'),
    )

    # Set amenities
    amenity_ids = data.get('amenity_ids', [])
    if amenity_ids:
        amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()
        place.amenities = amenities

    db.session.add(place)
    db.session.commit()

    lang = request.args.get('lang', 'ar')
    return jsonify({
        'message': 'Property created',
        'message_ar': 'تم إنشاء العقار',
        'place': place.to_dict(lang, include_private=True)
    }), 201


# ─── Update Place ────────────────────────────────────────────
@api_v1.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update property — owner or admin only"""
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    user = User.query.get(user_id)

    if place.owner_id != user_id and not (user and user.is_admin):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    updatable = [
        'title_en', 'title_ar', 'description_en', 'description_ar',
        'price_per_night', 'max_guests', 'bedrooms', 'bathrooms', 'beds',
        'trip_type', 'address', 'latitude', 'longitude',
        'access_instructions_en', 'access_instructions_ar',
        'floor_number', 'door_description_en', 'door_description_ar',
        'check_in_time', 'check_out_time', 'rules_en', 'rules_ar',
        'is_active', 'is_featured', 'monthly_discount',
    ]

    for field in updatable:
        if field in data:
            setattr(place, field, data[field])

    if 'amenity_ids' in data:
        amenities = Amenity.query.filter(Amenity.id.in_(data['amenity_ids'])).all()
        place.amenities = amenities

    db.session.commit()

    lang = request.args.get('lang', 'ar')
    return jsonify({
        'message': 'Property updated',
        'place': place.to_dict(lang, include_private=True)
    }), 200


# ─── Delete Place ────────────────────────────────────────────
@api_v1.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Soft delete property"""
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    user = User.query.get(user_id)

    if place.owner_id != user_id and not (user and user.is_admin):
        return jsonify({'error': 'Unauthorized'}), 403

    place.is_active = False
    db.session.commit()

    return jsonify({'message': 'Property deactivated', 'message_ar': 'تم تعطيل العقار'}), 200


# ─── Property Types ──────────────────────────────────────────
@api_v1.route('/property-types', methods=['GET'])
def list_property_types():
    """List all property types"""
    lang = request.args.get('lang', 'ar')
    types = PropertyType.query.order_by(PropertyType.sort_order).all()
    return jsonify([t.to_dict(lang) for t in types]), 200


# ─── Home Page Data ──────────────────────────────────────────
@api_v1.route('/home', methods=['GET'])
def home_data():
    """Aggregated home page data for the frontend"""
    lang = request.args.get('lang', 'ar')

    # Average price
    avg_price = db.session.query(func.avg(Place.price_per_night)) \
        .filter(Place.is_active == True).scalar() or 0

    # Cities
    cities = City.query.filter_by(is_featured=True).order_by(City.sort_order).all()

    # Featured / Elite
    featured = Place.query.filter_by(is_active=True, is_featured=True).limit(10).all()

    # Property Types
    types = PropertyType.query.order_by(PropertyType.sort_order).all()

    # Budget (below average)
    budget = Place.query.filter(
        Place.is_active == True,
        Place.price_per_night < avg_price
    ).order_by(Place.price_per_night.asc()).limit(10).all()

    # Monthly deals
    monthly = Place.query.filter(
        Place.is_active == True,
        Place.monthly_discount > 0
    ).limit(10).all()

    # Total counts
    total_places = Place.query.filter_by(is_active=True).count()

    return jsonify({
        'cities': [c.to_dict(lang) for c in cities],
        'featured': [p.to_card_dict(lang) for p in featured],
        'property_types': [t.to_dict(lang) for t in types],
        'budget_places': [p.to_card_dict(lang) for p in budget],
        'monthly_deals': [p.to_card_dict(lang) for p in monthly],
        'average_price': round(avg_price, 2),
        'total_places': total_places,
        'currency': 'SAR',
    }), 200
