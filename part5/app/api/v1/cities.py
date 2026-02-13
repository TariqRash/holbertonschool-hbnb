"""
HBnB V2 — Cities API
Saudi Arabia cities with Google Maps Places autocomplete.
"""
import requests as http_requests
from flask import request, jsonify, current_app
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


# ─── Google Maps Places Autocomplete ─────────────────────────
@api_v1.route('/cities/search', methods=['GET'])
def search_cities():
    """Search cities using Google Maps Places Autocomplete API.
    Falls back to database search if API key not available.
    """
    q = request.args.get('q', '').strip()
    lang = request.args.get('lang', 'ar')
    country = request.args.get('country', 'sa')

    if not q or len(q) < 2:
        return jsonify([]), 200

    api_key = current_app.config.get('GOOGLE_MAPS_API_KEY', '')

    if api_key:
        try:
            # Google Places Autocomplete
            autocomplete_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
            params = {
                'input': q,
                'types': '(cities)',
                'components': f'country:{country}',
                'language': lang,
                'key': api_key,
            }
            resp = http_requests.get(autocomplete_url, params=params, timeout=5)
            data = resp.json()

            if data.get('status') != 'OK':
                # Fall back to DB search
                return _db_search(q, lang)

            results = []
            for prediction in data.get('predictions', [])[:8]:
                place_id = prediction.get('place_id')
                description = prediction.get('description', '')

                # Get place details for lat/lng
                details = _get_place_details(place_id, api_key, lang)

                results.append({
                    'google_place_id': place_id,
                    'name': prediction.get('structured_formatting', {}).get('main_text', description),
                    'description': description,
                    'latitude': details.get('lat'),
                    'longitude': details.get('lng'),
                })

            return jsonify(results), 200

        except Exception:
            return _db_search(q, lang)
    else:
        return _db_search(q, lang)


def _get_place_details(place_id, api_key, lang='ar'):
    """Get place details (lat/lng) from Google Maps"""
    try:
        url = 'https://maps.googleapis.com/maps/api/place/details/json'
        params = {
            'place_id': place_id,
            'fields': 'geometry',
            'language': lang,
            'key': api_key,
        }
        resp = http_requests.get(url, params=params, timeout=5)
        data = resp.json()
        location = data.get('result', {}).get('geometry', {}).get('location', {})
        return {'lat': location.get('lat'), 'lng': location.get('lng')}
    except Exception:
        return {'lat': None, 'lng': None}


def _db_search(q, lang='ar'):
    """Fallback: search cities in local database"""
    if lang == 'ar':
        results = City.query.filter(
            db.or_(City.name_ar.ilike(f'%{q}%'), City.name_en.ilike(f'%{q}%'))
        ).limit(8).all()
    else:
        results = City.query.filter(
            db.or_(City.name_en.ilike(f'%{q}%'), City.name_ar.ilike(f'%{q}%'))
        ).limit(8).all()

    return jsonify([c.to_dict(lang) for c in results]), 200


# ─── Geocode Address ──────────────────────────────────────────
@api_v1.route('/cities/geocode', methods=['GET'])
def geocode_address():
    """Geocode an address using Google Maps Geocoding API"""
    address = request.args.get('address', '').strip()
    lang = request.args.get('lang', 'ar')

    if not address:
        return jsonify({'error': 'address parameter required'}), 400

    api_key = current_app.config.get('GOOGLE_MAPS_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'Google Maps API not configured'}), 500

    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': address,
            'region': 'sa',
            'language': lang,
            'key': api_key,
        }
        resp = http_requests.get(url, params=params, timeout=5)
        data = resp.json()

        if data.get('status') != 'OK' or not data.get('results'):
            return jsonify({'error': 'Address not found'}), 404

        result = data['results'][0]
        location = result['geometry']['location']

        return jsonify({
            'formatted_address': result.get('formatted_address', ''),
            'latitude': location.get('lat'),
            'longitude': location.get('lng'),
            'place_id': result.get('place_id'),
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
