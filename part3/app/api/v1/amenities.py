# Amenity API endpoints

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('amenities', description='Amenity operations')

# API models for documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    def get(self):
        """List all amenities (public endpoint)"""
        amenities = facade.get_all_amenities()
        return [{
            'id': str(a.id),
            'name': a.name
        } for a in amenities], 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.doc('create_amenity')
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        
        data = request.get_json() or {}
        if "name" not in data:
            return {"error": "Missing required fields"}, 400
        
        existing = facade.get_amenity_by_name(data["name"])
        if existing:
            return {"error": "Amenity already exists"}, 400
        
        amenity = facade.create_amenity({"name": data["name"]})
        return {"id": str(amenity.id), "message": "Amenity created successfully"}, 201


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    def get(self, amenity_id):
        """Get an amenity by ID (public endpoint)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        
        return {
            "id": str(amenity.id),
            "name": amenity.name,
            "created_at": amenity.created_at.isoformat() if amenity.created_at else None,
            "updated_at": amenity.updated_at.isoformat() if amenity.updated_at else None
        }, 200

    @jwt_required()
    @api.doc('update_amenity')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        
        data = request.get_json() or {}
        if "name" not in data:
            return {"error": "Missing required fields"}, 400
        
        existing = facade.get_amenity_by_name(data["name"])
        if existing and str(existing.id) != amenity_id:
            return {"error": "Amenity already exists"}, 400
        
        facade.update_amenity(amenity_id, {"name": data["name"]})
        return {"message": "Amenity updated successfully"}, 200
