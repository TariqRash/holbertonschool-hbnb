"""
HBnB V2 — Cities API
Saudi Arabia cities listing.
"""
from flask import request, jsonify
from app.api.v1 import api_v1
from app import db
from app.models.city import City


@api_v1.route('/cities', methods=['GET'])
def list_cities():
    """List all cities"""
    lang = request.args.get('lang', 'ar')
    featured_only = request.args.get('featured', '').lower() == 'true'

    query = City.query
    if featured_only:
        query = query.filter_by(is_featured=True)

    cities = query.order_by(City.sort_order, City.name_en).all()
    return jsonify([c.to_dict(lang) for c in cities]), 200


@api_v1.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Get city details with place count"""
    lang = request.args.get('lang', 'ar')
    city = City.query.get_or_404(city_id)
    return jsonify(city.to_dict(lang)), 200
