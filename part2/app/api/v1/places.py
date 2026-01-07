"""Place API endpoints"""
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', min_length=5, max_length=100),
    'description': fields.String(required=True, description='Place description', max_length=1000),
    'price': fields.Float(required=True, description='Price per night', min=0),
    'latitude': fields.Float(required=True, description='Latitude', min=-90, max=90),
    'longitude': fields.Float(required=True, description='Longitude', min=-180, max=180),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = place.to_dict()
            # Add extended attributes
            place_dict['owner'] = {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            }
            place_dict['amenities'] = [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ]
            result.append(place_dict)
        return result, 200

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(api.payload)
            place_dict = place.to_dict()
            # Add extended attributes
            place_dict['owner'] = {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            }
            place_dict['amenities'] = [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ]
            return place_dict, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        place_dict = place.to_dict()
        # Add extended attributes
        place_dict['owner'] = {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        }
        place_dict['amenities'] = [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in place.amenities
        ]
        return place_dict, 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update a place"""
        place = facade.update_place(place_id, api.payload)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict(), 200
