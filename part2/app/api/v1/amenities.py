"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name', min_length=3, max_length=50),
    'description': fields.String(description='Amenity description', max_length=200)
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200
