from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True),
        "name": fields.String(required=True),
        "description": fields.String,
    },
)


@api.route("")
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return [a.to_dict() for a in facade.list_amenities()]

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=HTTPStatus.CREATED)
    def post(self):
        data = request.get_json(force=True)
        amenity = facade.create_amenity(
            name=data.get("name"), description=data.get("description")
        )
        return amenity.to_dict(), HTTPStatus.CREATED


@api.route("/<string:amenity_id>")
@api.response(HTTPStatus.NOT_FOUND, "Amenity not found")
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id: str):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(HTTPStatus.NOT_FOUND, "Amenity not found")
        return amenity.to_dict()

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id: str):
        data = request.get_json(force=True)
        amenity = facade.update_amenity(
            amenity_id, name=data.get("name"), description=data.get("description")
        )
        if not amenity:
            api.abort(HTTPStatus.NOT_FOUND, "Amenity not found")
        return amenity.to_dict()
