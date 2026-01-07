"""Review API endpoints"""
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'comment': fields.String(required=True, description='Review comment', max_length=500)
})


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    def get(self):
        """List all reviews"""
        reviews = facade.get_all_reviews()
        result = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add extended attributes
            review_dict['user'] = {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name
            }
            review_dict['place'] = {
                'id': review.place.id,
                'title': review.place.title
            }
            result.append(review_dict)
        return result, 200

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review"""
        try:
            review = facade.create_review(api.payload)
            review_dict = review.to_dict()
            # Add extended attributes
            review_dict['user'] = {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name
            }
            review_dict['place'] = {
                'id': review.place.id,
                'title': review.place.title
            }
            return review_dict, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.doc('get_review')
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        review_dict = review.to_dict()
        # Add extended attributes
        review_dict['user'] = {
            'id': review.user.id,
            'first_name': review.user.first_name,
            'last_name': review.user.last_name
        }
        review_dict['place'] = {
            'id': review.place.id,
            'title': review.place.title
        }
        return review_dict, 200

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update a review"""
        review = facade.update_review(review_id, api.payload)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict(), 200

    @api.doc('delete_review')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, 'Review not found')
        return '', 204


@api.route('/places/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        result = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add extended attributes
            review_dict['user'] = {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name
            }
            result.append(review_dict)
        return result, 200
