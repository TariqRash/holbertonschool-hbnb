# Review API endpoints

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('reviews', description='Review operations')

# API models for documentation
review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='Place ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating 1-5')
})


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    def get(self):
        """List all reviews (public endpoint)"""
        reviews = facade.get_all_reviews()
        return [{
            'id': str(r.id),
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'place_id': r.place_id,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in reviews], 200

    @jwt_required()
    @api.expect(review_model)
    @api.doc('create_review')
    def post(self):
        """Create a new review (authenticated users)"""
        data = request.get_json()
        required_fields = ["place_id", "text", "rating"]
        if not data or not all(f in data for f in required_fields):
            return {"error": "Missing required fields"}, 400
        
        # Validate rating
        if not (1 <= data['rating'] <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400
        
        current_user_id = get_jwt_identity()
        place = facade.get_place(data["place_id"])
        
        if not place:
            return {"error": "Place not found"}, 404
        
        # Cannot review own place
        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place"}, 400
        
        # Cannot review same place twice
        existing_review = facade.get_review_by_user_and_place(current_user_id, data["place_id"])
        if existing_review:
            return {"error": "You have already reviewed this place"}, 400
        
        review_data = {
            "user_id": current_user_id,
            "place_id": data["place_id"],
            "text": data["text"],
            "rating": data["rating"]
        }
        review = facade.create_review(review_data)
        return {"id": str(review.id), "message": "Review created successfully"}, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.doc('get_review')
    def get(self, review_id):
        """Get a review by ID (public endpoint)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        return {
            "id": str(review.id),
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "created_at": review.created_at.isoformat() if review.created_at else None,
            "updated_at": review.updated_at.isoformat() if review.updated_at else None
        }, 200

    @jwt_required()
    @api.doc('update_review')
    def put(self, review_id):
        """Update a review (owner or admin only)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        if not is_admin and review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
        
        data = request.get_json() or {}
        allowed_fields = ["text", "rating"]
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Validate rating if provided
        if "rating" in update_data and not (1 <= update_data["rating"] <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400
        
        if update_data:
            facade.update_review(review_id, update_data)
        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    @api.doc('delete_review')
    def delete(self, review_id):
        """Delete a review (owner or admin only)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        if not is_admin and review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
        
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
