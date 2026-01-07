"""User API endpoints"""
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name', min_length=2, max_length=50),
    'last_name': fields.String(required=True, description='User last name', min_length=2, max_length=50),
    'email': fields.String(required=True, description='User email address'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200

    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        user = facade.update_user(user_id, api.payload)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200
