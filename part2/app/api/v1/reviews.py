from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "id": fields.String(readonly=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
        "rating": fields.Integer(required=True, min=1, max=5),
        "text": fields.String,
    },
)


@api.route("")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        return [r.to_dict() for r in facade.list_reviews()]

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=HTTPStatus.CREATED)
    def post(self):
        data = request.get_json(force=True)
        review = facade.create_review(
            user_id=data.get("user_id"),
            place_id=data.get("place_id"),
            rating=data.get("rating"),
            text=data.get("text"),
        )
        if not review:
            api.abort(HTTPStatus.BAD_REQUEST, "User or place not found")
        return review.to_dict(), HTTPStatus.CREATED


@api.route("/<string:review_id>")
@api.response(HTTPStatus.NOT_FOUND, "Review not found")
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id: str):
        review = facade.get_review(review_id)
        if not review:
            api.abort(HTTPStatus.NOT_FOUND, "Review not found")
        return review.to_dict()

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id: str):
        data = request.get_json(force=True)
        review = facade.update_review(
            review_id,
            user_id=data.get("user_id"),
            place_id=data.get("place_id"),
            rating=data.get("rating"),
            text=data.get("text"),
        )
        if review is None:
            api.abort(HTTPStatus.NOT_FOUND, "Review not found")
        if review is False:
            api.abort(HTTPStatus.BAD_REQUEST, "User or place not found")
        return review.to_dict()

    @api.response(HTTPStatus.NO_CONTENT, "Deleted")
    def delete(self, review_id: str):
        deleted = facade.delete_review(review_id)
        if not deleted:
            api.abort(HTTPStatus.NOT_FOUND, "Review not found")
        return "", HTTPStatus.NO_CONTENT
