# Auth API endpoints

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace('auth', description='Authentication operations')

# API models for documentation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.doc('register')
    def post(self):
        """Register a new user (public endpoint)"""
        data = request.get_json()

        required_fields = ["first_name", "last_name", "email", "password"]
        if not data or not all(f in data for f in required_fields):
            return {"error": "Missing required fields"}, 400

        if facade.get_user_by_email(data["email"]):
            return {"error": "Email already registered"}, 400

        user = facade.create_user(data)
        return {"id": str(user.id), "message": "User created successfully"}, 201


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.doc('login')
    def post(self):
        """Authenticate user and return a JWT token"""
        data = request.get_json()
        
        if not data or "email" not in data or "password" not in data:
            return {"error": "Invalid credentials"}, 401
        
        user = facade.get_user_by_email(data["email"])
        
        if not user or not user.verify_password(data["password"]):
            return {"error": "Invalid credentials"}, 401
        
        # Create JWT token with user identity and admin claim
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {"access_token": access_token}, 200
