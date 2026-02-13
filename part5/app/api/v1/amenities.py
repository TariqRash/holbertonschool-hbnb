"""
HBnB V2 — Amenities API
With icons support.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.amenity import Amenity
from app.models.user import User


@api_v1.route('/amenities', methods=['GET'])
def list_amenities():
    """List all amenities with icons"""
    lang = request.args.get('lang', 'ar')
    category = request.args.get('category')

    query = Amenity.query
    if category:
        query = query.filter_by(category=category)

    amenities = query.order_by(Amenity.category, Amenity.sort_order).all()
    return jsonify([a.to_dict(lang) for a in amenities]), 200


@api_v1.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    """Create amenity — admin only"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    amenity = Amenity(
        name_en=data['name_en'],
        name_ar=data['name_ar'],
        icon=data.get('icon'),
        category=data.get('category', 'general'),
    )

    db.session.add(amenity)
    db.session.commit()

    return jsonify(amenity.to_dict()), 201
