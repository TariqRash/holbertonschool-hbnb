from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade

api = Namespace("users", description="User operations")

user_payload = api.model(
    "UserPayload",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "first_name": fields.String,
        "last_name": fields.String,
        "is_admin": fields.Boolean,
    },
)

user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True),
        "email": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "is_admin": fields.Boolean,
    },
)


@api.route("")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return [u.to_dict() for u in facade.list_users()]

    @api.expect(user_payload, validate=True)
    @api.marshal_with(user_model, code=HTTPStatus.CREATED)
    def post(self):
        data = request.get_json(force=True)
        user = facade.create_user(
            email=data.get("email"),
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            is_admin=data.get("is_admin", False),
        )
        return user.to_dict(), HTTPStatus.CREATED


@api.route("/<string:user_id>")
@api.response(HTTPStatus.NOT_FOUND, "User not found")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id: str):
        user = facade.get_user(user_id)
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, "User not found")
        return user.to_dict()

    @api.expect(user_payload, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id: str):
        data = request.get_json(force=True)
        user = facade.update_user(
            user_id,
            email=data.get("email"),
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            is_admin=data.get("is_admin"),
        )
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, "User not found")
        return user.to_dict()
