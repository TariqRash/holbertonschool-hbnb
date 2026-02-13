"""
HBnB V2 — Admin API
Full CRUD for all entities + site settings management.
All endpoints require admin role.
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.api.v1 import api_v1
from app import db
from app.models.user import User
from app.models.place import Place, PropertyType
from app.models.booking import Booking
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.city import City
from app.models.payment import Payment
from app.models.media import Media
from app.models.site_settings import SiteSetting


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required', 'error_ar': 'صلاحية المدير مطلوبة'}), 403
        return fn(*args, **kwargs)
    return wrapper


# ═══════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    """Get admin dashboard stats"""
    return jsonify({
        'users': User.query.count(),
        'places': Place.query.count(),
        'bookings': Booking.query.count(),
        'reviews': Review.query.count(),
        'amenities': Amenity.query.count(),
        'cities': City.query.count(),
        'property_types': PropertyType.query.count(),
        'active_bookings': Booking.query.filter(Booking.status.in_(['confirmed', 'checked_in'])).count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).filter(Payment.status == 'completed').scalar() or 0,
        'pending_bookings': Booking.query.filter_by(status='pending').count(),
    }), 200


# ═══════════════════════════════════════════════════════════
# USERS CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/users', methods=['GET'])
@admin_required
def admin_list_users():
    """List all users with filters"""
    role = request.args.get('role')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = User.query
    if role:
        query = query.filter_by(role=role)
    if search:
        query = query.filter(
            db.or_(
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
            )
        )

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'users': [u.to_dict(include_private=True) for u in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
    }), 200


@api_v1.route('/admin/users', methods=['POST'])
@admin_required
def admin_create_user():
    """Create a new user"""
    data = request.get_json()
    if not data.get('email'):
        return jsonify({'error': 'Email required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        email=data['email'],
        phone=data.get('phone'),
        role=data.get('role', 'guest'),
        is_active=data.get('is_active', True),
        is_verified=data.get('is_verified', True),
        preferred_language=data.get('preferred_language', 'ar'),
        country=data.get('country', 'SA'),
    )
    if data.get('password'):
        user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user': user.to_dict(include_private=True)}), 201


@api_v1.route('/admin/users/<user_id>', methods=['PUT'])
@admin_required
def admin_update_user(user_id):
    """Update a user"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    for field in ['first_name', 'last_name', 'email', 'phone', 'role', 'is_active', 'is_verified', 'preferred_language', 'country', 'bio']:
        if field in data:
            setattr(user, field, data[field])
    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict(include_private=True)}), 200


@api_v1.route('/admin/users/<user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    """Deactivate a user (soft delete)"""
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'User deactivated'}), 200


# ═══════════════════════════════════════════════════════════
# PLACES CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/places', methods=['GET'])
@admin_required
def admin_list_places():
    """List all places"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    lang = request.args.get('lang', 'ar')

    query = Place.query
    if search:
        query = query.filter(
            db.or_(
                Place.title_ar.ilike(f'%{search}%'),
                Place.title_en.ilike(f'%{search}%'),
            )
        )

    pagination = query.order_by(Place.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({
        'places': [p.to_dict(lang) for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
    }), 200


@api_v1.route('/admin/places/<place_id>', methods=['GET'])
@admin_required
def admin_get_place(place_id):
    """Get full place details for admin editing"""
    place = Place.query.get_or_404(place_id)
    data = place.to_dict('ar', include_private=True)
    # Add admin-only fields
    data['description_ar'] = place.description_ar
    data['description_en'] = place.description_en
    data['monthly_discount'] = place.monthly_discount
    data['is_active'] = place.is_active
    data['instant_book'] = place.is_instant_book
    return jsonify(data), 200


@api_v1.route('/admin/places/<place_id>', methods=['PUT'])
@admin_required
def admin_update_place(place_id):
    """Update any place"""
    place = Place.query.get_or_404(place_id)
    data = request.get_json()

    fields = ['title_ar', 'title_en', 'description_ar', 'description_en',
              'price_per_night', 'monthly_discount', 'city_id', 'property_type_id',
              'bedrooms', 'bathrooms', 'max_guests', 'beds',
              'is_active', 'is_featured', 'trip_type',
              'latitude', 'longitude', 'address', 'check_in_time', 'check_out_time']

    for field in fields:
        if field in data:
            setattr(place, field, data[field])

    # Handle instant_book alias -> is_instant_book column
    if 'instant_book' in data:
        place.is_instant_book = data['instant_book']

    db.session.commit()
    return jsonify({'message': 'Place updated', 'place': place.to_dict()}), 200


@api_v1.route('/admin/places/<place_id>', methods=['DELETE'])
@admin_required
def admin_delete_place(place_id):
    """Deactivate a place (soft delete)"""
    place = Place.query.get_or_404(place_id)
    place.is_active = False
    db.session.commit()
    return jsonify({'message': 'Place deactivated'}), 200


# ═══════════════════════════════════════════════════════════
# BOOKINGS CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/bookings', methods=['GET'])
@admin_required
def admin_list_bookings():
    """List all bookings"""
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)

    query = Booking.query
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({
        'bookings': [b.to_dict() for b in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
    }), 200


@api_v1.route('/admin/bookings/<booking_id>', methods=['PUT'])
@admin_required
def admin_update_booking(booking_id):
    """Update booking status"""
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()

    for field in ['status', 'check_in', 'check_out', 'total_price', 'special_requests']:
        if field in data:
            setattr(booking, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Booking updated', 'booking': booking.to_dict()}), 200


@api_v1.route('/admin/bookings/<booking_id>', methods=['DELETE'])
@admin_required
def admin_cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Booking cancelled'}), 200


# ═══════════════════════════════════════════════════════════
# REVIEWS CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/reviews', methods=['GET'])
@admin_required
def admin_list_reviews():
    """List all reviews"""
    page = request.args.get('page', 1, type=int)
    approved = request.args.get('approved')

    query = Review.query
    if approved is not None:
        query = query.filter_by(is_approved=approved.lower() == 'true')

    pagination = query.order_by(Review.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({
        'reviews': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
    }), 200


@api_v1.route('/admin/reviews/<review_id>', methods=['PUT'])
@admin_required
def admin_update_review(review_id):
    """Approve/reject a review"""
    review = Review.query.get_or_404(review_id)
    data = request.get_json()

    if 'is_approved' in data:
        review.is_approved = data['is_approved']
    if 'comment' in data:
        review.comment = data['comment']

    db.session.commit()
    return jsonify({'message': 'Review updated', 'review': review.to_dict()}), 200


@api_v1.route('/admin/reviews/<review_id>', methods=['DELETE'])
@admin_required
def admin_delete_review(review_id):
    """Delete a review"""
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200


# ═══════════════════════════════════════════════════════════
# AMENITIES CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/amenities', methods=['GET'])
@admin_required
def admin_list_amenities():
    """List all amenities"""
    amenities = Amenity.query.order_by(Amenity.category, Amenity.sort_order).all()
    return jsonify([a.to_dict() for a in amenities]), 200


@api_v1.route('/admin/amenities', methods=['POST'])
@admin_required
def admin_create_amenity():
    """Create an amenity"""
    data = request.get_json()
    amenity = Amenity(
        name_en=data['name_en'],
        name_ar=data['name_ar'],
        icon=data.get('icon', ''),
        category=data.get('category', 'general'),
        sort_order=data.get('sort_order', 0),
    )
    db.session.add(amenity)
    db.session.commit()
    return jsonify({'message': 'Amenity created', 'amenity': amenity.to_dict()}), 201


@api_v1.route('/admin/amenities/<amenity_id>', methods=['PUT'])
@admin_required
def admin_update_amenity(amenity_id):
    """Update an amenity"""
    amenity = Amenity.query.get_or_404(amenity_id)
    data = request.get_json()

    for field in ['name_en', 'name_ar', 'icon', 'category', 'sort_order']:
        if field in data:
            setattr(amenity, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Amenity updated', 'amenity': amenity.to_dict()}), 200


@api_v1.route('/admin/amenities/<amenity_id>', methods=['DELETE'])
@admin_required
def admin_delete_amenity(amenity_id):
    """Delete an amenity"""
    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({'message': 'Amenity deleted'}), 200


# ═══════════════════════════════════════════════════════════
# CITIES CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/cities', methods=['GET'])
@admin_required
def admin_list_cities():
    """List all cities"""
    cities = City.query.order_by(City.sort_order).all()
    return jsonify([c.to_dict() for c in cities]), 200


@api_v1.route('/admin/cities', methods=['POST'])
@admin_required
def admin_create_city():
    """Create a city"""
    data = request.get_json()
    city = City(
        name_en=data['name_en'],
        name_ar=data['name_ar'],
        region_en=data.get('region_en', ''),
        region_ar=data.get('region_ar', ''),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        is_featured=data.get('is_featured', False),
        sort_order=data.get('sort_order', 0),
    )
    db.session.add(city)
    db.session.commit()
    return jsonify({'message': 'City created', 'city': city.to_dict()}), 201


@api_v1.route('/admin/cities/<city_id>', methods=['PUT'])
@admin_required
def admin_update_city(city_id):
    """Update a city"""
    city = City.query.get_or_404(city_id)
    data = request.get_json()

    for field in ['name_en', 'name_ar', 'region_en', 'region_ar', 'latitude', 'longitude', 'image_url', 'is_featured', 'sort_order']:
        if field in data:
            setattr(city, field, data[field])

    db.session.commit()
    return jsonify({'message': 'City updated', 'city': city.to_dict()}), 200


@api_v1.route('/admin/cities/<city_id>', methods=['DELETE'])
@admin_required
def admin_delete_city(city_id):
    """Delete a city"""
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return jsonify({'message': 'City deleted'}), 200


# ═══════════════════════════════════════════════════════════
# PROPERTY TYPES CRUD
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/property-types', methods=['GET'])
@admin_required
def admin_list_property_types():
    """List all property types"""
    types = PropertyType.query.order_by(PropertyType.sort_order).all()
    return jsonify([t.to_dict() for t in types]), 200


@api_v1.route('/admin/property-types', methods=['POST'])
@admin_required
def admin_create_property_type():
    """Create a property type"""
    data = request.get_json()
    pt = PropertyType(
        name_en=data['name_en'],
        name_ar=data['name_ar'],
        icon=data.get('icon', ''),
        image_url=data.get('image_url'),
        sort_order=data.get('sort_order', 0),
    )
    db.session.add(pt)
    db.session.commit()
    return jsonify({'message': 'Property type created', 'property_type': pt.to_dict()}), 201


@api_v1.route('/admin/property-types/<pt_id>', methods=['PUT'])
@admin_required
def admin_update_property_type(pt_id):
    """Update a property type"""
    pt = PropertyType.query.get_or_404(pt_id)
    data = request.get_json()

    for field in ['name_en', 'name_ar', 'icon', 'image_url', 'sort_order']:
        if field in data:
            setattr(pt, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Property type updated', 'property_type': pt.to_dict()}), 200


@api_v1.route('/admin/property-types/<pt_id>', methods=['DELETE'])
@admin_required
def admin_delete_property_type(pt_id):
    """Delete a property type"""
    pt = PropertyType.query.get_or_404(pt_id)
    db.session.delete(pt)
    db.session.commit()
    return jsonify({'message': 'Property type deleted'}), 200


# ═══════════════════════════════════════════════════════════
# SITE SETTINGS
# ═══════════════════════════════════════════════════════════

@api_v1.route('/admin/settings', methods=['GET'])
@admin_required
def admin_list_settings():
    """List all site settings"""
    category = request.args.get('category')
    query = SiteSetting.query
    if category:
        query = query.filter_by(category=category)

    settings = query.order_by(SiteSetting.category, SiteSetting.key).all()
    return jsonify([s.to_dict(include_secrets=True) for s in settings]), 200


@api_v1.route('/admin/settings', methods=['POST'])
@admin_required
def admin_create_setting():
    """Create or update a site setting"""
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify({'error': 'Key required'}), 400

    setting = SiteSetting.set_value(
        key=key,
        value=data.get('value', ''),
        category=data.get('category', 'general'),
        description_en=data.get('description_en'),
        description_ar=data.get('description_ar'),
        is_secret=data.get('is_secret', False),
    )

    return jsonify({'message': 'Setting saved', 'setting': setting.to_dict(include_secrets=True)}), 200


@api_v1.route('/admin/settings/<setting_id>', methods=['PUT'])
@admin_required
def admin_update_setting(setting_id):
    """Update a site setting"""
    setting = SiteSetting.query.get_or_404(setting_id)
    data = request.get_json()

    for field in ['key', 'value', 'category', 'description_en', 'description_ar', 'is_secret']:
        if field in data:
            setattr(setting, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Setting updated', 'setting': setting.to_dict(include_secrets=True)}), 200


@api_v1.route('/admin/settings/<setting_id>', methods=['DELETE'])
@admin_required
def admin_delete_setting(setting_id):
    """Delete a site setting"""
    setting = SiteSetting.query.get_or_404(setting_id)
    db.session.delete(setting)
    db.session.commit()
    return jsonify({'message': 'Setting deleted'}), 200


# ═══════════════════════════════════════════════════════════
# CONFIG ENDPOINT (for frontend to read public settings)
# ═══════════════════════════════════════════════════════════

@api_v1.route('/config', methods=['GET'])
def get_public_config():
    """Get public configuration for the frontend"""
    return jsonify({
        'google_maps_api_key': current_app.config.get('GOOGLE_MAPS_API_KEY', ''),
        'stripe_publishable_key': current_app.config.get('STRIPE_PUBLISHABLE_KEY', ''),
        'check_in_time': current_app.config.get('CHECK_IN_TIME', '16:00'),
        'check_out_time': current_app.config.get('CHECK_OUT_TIME', '12:00'),
        'cleaning_hours': current_app.config.get('CLEANING_HOURS', 4),
        'app_name': current_app.config.get('APP_NAME', 'Rizi'),
        'domain': current_app.config.get('DOMAIN', 'rizi.app'),
        'default_language': current_app.config.get('DEFAULT_LANGUAGE', 'ar'),
    }), 200
