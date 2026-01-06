from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_payload = api.model(
    "PlacePayload",
    {
        "title": fields.String(required=True),
        "description": fields.String,
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner_id": fields.String(required=True),
        "amenity_ids": fields.List(fields.String, default=[]),
    },
)

place_model = api.model(
    "Place",
    {
        "id": fields.String(readonly=True),
        "title": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "owner_id": fields.String,
        "amenity_ids": fields.List(fields.String),
        "owner": fields.Raw,
        "amenities": fields.List(fields.Raw),
    },
)


def _serialize_place(place):
    data = place.to_dict()
    owner = facade.get_user(place.owner_id)
    data["owner"] = owner.to_dict() if owner else None
    amenities = [facade.get_amenity(aid) for aid in place.amenity_ids]
    data["amenities"] = [a.to_dict() for a in amenities if a]
    return data


@api.route("")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        return [_serialize_place(p) for p in facade.list_places()]

    @api.expect(place_payload, validate=True)
    @api.marshal_with(place_model, code=HTTPStatus.CREATED)
    def post(self):
        data = request.get_json(force=True)
        place = facade.create_place(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=data.get("owner_id"),
            amenity_ids=data.get("amenity_ids") or [],
        )
        if not place:
            api.abort(HTTPStatus.BAD_REQUEST, "Owner or amenity not found")
        return _serialize_place(place), HTTPStatus.CREATED


@api.route("/<string:place_id>")
@api.response(HTTPStatus.NOT_FOUND, "Place not found")
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id: str):
        place = facade.get_place(place_id)
        if not place:
            api.abort(HTTPStatus.NOT_FOUND, "Place not found")
        return _serialize_place(place)

    @api.expect(place_payload, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id: str):
        data = request.get_json(force=True)
        place = facade.update_place(
            place_id,
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=data.get("owner_id"),
            amenity_ids=data.get("amenity_ids") or [],
        )
        if place is None:
            api.abort(HTTPStatus.NOT_FOUND, "Place not found")
        if place is False:
            api.abort(HTTPStatus.BAD_REQUEST, "Owner or amenity not found")
        return _serialize_place(place)


@api.route("/<string:place_id>/reviews")
@api.response(HTTPStatus.NOT_FOUND, "Place not found")
class PlaceReviews(Resource):
    def get(self, place_id: str):
        reviews = facade.list_reviews_for_place(place_id)
        if reviews is None:
            api.abort(HTTPStatus.NOT_FOUND, "Place not found")
        return [r.to_dict() for r in reviews]
