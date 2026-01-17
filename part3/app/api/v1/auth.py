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
