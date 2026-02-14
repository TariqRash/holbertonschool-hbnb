"""
HBnB V2 — Users API
Admin user management.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.user import User


@api_v1.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """List users — admin only"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict(include_private=True) for u in users]), 200


@api_v1.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    """Get user public profile"""
    user = User.query.get_or_404(uid)
    return jsonify(user.to_public_dict()), 200


@api_v1.route('/users/<uid>/places', methods=['GET'])
def user_places(uid):
    """Get places owned by a user"""
    lang = request.args.get('lang', 'ar')
    user = User.query.get_or_404(uid)

    if not user.is_owner:
        return jsonify({'places': []}), 200

    from app.models.place import Place
    places = Place.query.filter_by(owner_id=uid, is_active=True).all()
    return jsonify({
        'owner': user.to_public_dict(),
        'places': [p.to_card_dict(lang) for p in places]
    }), 200


@api_v1.route('/users/favorites/<place_id>', methods=['POST'])
@jwt_required()
def add_favorite(place_id):
    """Add place to favorites"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    from app.models.place import Place
    place = Place.query.get_or_404(place_id)

    if place not in user.favorites:
        user.favorites.append(place)
        db.session.commit()
    
    return jsonify({'message': 'Added to favorites'}), 200


@api_v1.route('/users/favorites/<place_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(place_id):
    """Remove place from favorites"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    from app.models.place import Place
    place = Place.query.get_or_404(place_id)

    if place in user.favorites:
        user.favorites.remove(place)
        db.session.commit()
    
    return jsonify({'message': 'Removed from favorites'}), 200


@api_v1.route('/users/favorites', methods=['GET'])
@jwt_required()
def list_favorites():
    """List user favorites"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    lang = request.args.get('lang', 'ar')
    
    return jsonify({
        'favorites': [p.to_card_dict(lang) for p in user.favorites]
    }), 200
