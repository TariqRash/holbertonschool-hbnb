# Place API endpoints

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('places', description='Place operations')

# API models for documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """List all places (public endpoint)"""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_data = {
                'id': str(place.id),
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id
            }
            # Include owner info if available
            if place.owner:
                place_data['owner'] = {
                    'id': str(place.owner.id),
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                }
            result.append(place_data)
        return result, 200

    @jwt_required()
    @api.expect(place_model)
    @api.doc('create_place')
    def post(self):
        """Create a new place (authenticated users)"""
        data = request.get_json()
        required_fields = ["title", "description", "price", "latitude", "longitude"]
        if not data or not all(f in data for f in required_fields):
            return {"error": "Missing required fields"}, 400
        
        # Validate price
        if data['price'] <= 0:
            return {"error": "Price must be positive"}, 400
        
        # Validate latitude/longitude
        if not (-90 <= data['latitude'] <= 90):
            return {"error": "Latitude must be between -90 and 90"}, 400
        if not (-180 <= data['longitude'] <= 180):
            return {"error": "Longitude must be between -180 and 180"}, 400
        
        owner_id = get_jwt_identity()
        place_data = {
            "title": data["title"],
            "description": data["description"],
            "price": data["price"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "owner_id": owner_id
        }
        place = facade.create_place(place_data)
        
        # Handle amenities if provided
        if "amenities" in data and data["amenities"]:
            for amenity_id in data["amenities"]:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
        
        return {"id": str(place.id), "message": "Place created successfully"}, 201


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get a place by ID (public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        result = {
            "id": str(place.id),
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "created_at": place.created_at.isoformat() if place.created_at else None,
            "updated_at": place.updated_at.isoformat() if place.updated_at else None
        }
        
        # Include owner info
        if place.owner:
            result['owner'] = {
                'id': str(place.owner.id),
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            }
        
        # Include amenities
        result['amenities'] = [{
            'id': str(a.id),
            'name': a.name
        } for a in place.amenities] if place.amenities else []
        
        # Include reviews
        result['reviews'] = [{
            'id': str(r.id),
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id
        } for r in place.reviews] if place.reviews else []
        
        return result, 200

    @jwt_required()
    @api.doc('update_place')
    def put(self, place_id):
        """Update a place (owner or admin only)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()
        
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        # Check ownership or admin
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
        
        data = request.get_json() or {}
        allowed_fields = ["title", "description", "price", "latitude", "longitude"]
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if update_data:
            facade.update_place(place_id, update_data)
        return {"message": "Place updated successfully"}, 200

    @jwt_required()
    @api.doc('delete_place')
    def delete(self, place_id):
        """Delete a place (owner or admin only)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()
        
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
        
        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200


@api.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    def get(self, place_id):
        """Get all reviews for a place (public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': str(r.id),
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in reviews], 200
