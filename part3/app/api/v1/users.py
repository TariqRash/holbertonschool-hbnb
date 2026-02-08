# User API endpoints

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('users', description='User operations')

# API models for documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

user_response = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """List all users (public endpoint)"""
        users = facade.get_all_users()
        return [{
            'id': str(u.id),
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'is_admin': u.is_admin
        } for u in users], 200

    @jwt_required()
    @api.expect(user_model)
    @api.doc('create_user')
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        
        data = request.get_json()
        required_fields = ["first_name", "last_name", "email", "password"]
        if not data or not all(f in data for f in required_fields):
            return {"error": "Missing required fields"}, 400
        
        if facade.get_user_by_email(data["email"]):
            return {"error": "Email already registered"}, 400
        
        user = facade.create_user(data)
        return {"id": str(user.id), "message": "User created successfully"}, 201


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, user_id):
        """Get a user by ID (public endpoint, password excluded)"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        return {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }, 200

    @jwt_required()
    @api.doc('update_user')
    def put(self, user_id):
        """Update a user (self or admin)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()
        
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        data = request.get_json() or {}
        
        if is_admin:
            # Admin can update any field including email/password
            if "email" in data:
                existing = facade.get_user_by_email(data["email"])
                if existing and str(existing.id) != user_id:
                    return {"error": "Email is already in use"}, 400
            facade.admin_update_user(user_id, data)
            return {"message": "User updated successfully"}, 200
        else:
            # Regular users can only update their own profile
            if current_user_id != user_id:
                return {"error": "Unauthorized action"}, 403
            
            # Regular users cannot modify email or password
            if "email" in data or "password" in data:
                return {"error": "You cannot modify email or password"}, 400
            
            allowed_fields = ["first_name", "last_name"]
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if update_data:
                facade.update_user(user_id, update_data)
            return {"message": "User updated successfully"}, 200
